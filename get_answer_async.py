import json
import logging
import random

import aiohttp
from bs4 import BeautifulSoup
from itertools import combinations, product
from fake_headers import Headers

logger = logging.getLogger(__name__)


async def get_fake_test_url(url, session):
    headers = (
        Headers(browser="chrome", os="win", headers=True)
        .generate()
        .update(
            {
                "authority": "videouroki.net",
            }
        )
    )
    async with session.get(url=url, headers=headers) as resp:
        page = await resp.text()
        soup = BeautifulSoup(page, features="html.parser")
    test_title = soup.find("p", class_="test_header__ui_testname").get_text()
    del soup

    headers = (
        Headers(browser="chrome", os="win", headers=True)
        .generate()
        .update(
            {
                "pragma": "no-cache",
                "referer": "https://videouroki.net/",
                "authority": "cse.google.com",
                "sec-fetch-dest": "script",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "cross-site",
            }
        )
    )

    search_url = (
        f"https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=ru&source=gcsc&gss=."
        f"com&cselibv=c20e9fb0a344f1f9&cx=002726216306166405977:gcagx71gt_c&q={test_title}&"
        f"safe=off&cse_tok=ALwrddHJmfJF5mP-4xx0Kl38mgX7:1674799158435&sort=&exp=csqr,"
        f"cc&callback=google.search.cse.api18418"
    )

    async with session.get(url=search_url, headers=headers) as resp:
        response = await resp.text()
    search_res = response.replace("/*O_o*/\ngoogle.search.cse.api18418(", "")[:-2]

    search_res = json.loads(search_res)
    test_page_url = search_res["results"][0]["url"]
    del search_res
    async with session.get(url=test_page_url, headers=headers) as resp:
        response = await resp.text()
    test_page = BeautifulSoup(response, features="html.parser")
    url_fake_test_a = test_page.find("a", class_="btn blue", attrs={"rel": "nofollow"})

    fake_test_url = "https://videouroki.net" + url_fake_test_a["href"]
    return fake_test_url, test_title, test_page_url


async def save_ans(q_id, type, member, variants, session, headers):
    json_data = {
        "answer": {
            "id": q_id,
            "variants": variants[0] if type == 1 else variants,
        },
        "member": member,
    }

    async with session.get(
        url=f'https://videouroki.net/tests/api/save/{member["fakeId"]}/',
        headers=headers,
        json=json_data,
    ) as resp:
        await resp.json()


async def create_member(test_id, session, headers):
    json_data = {
        "member": {
            "id": False,
            "lastname": str(random.randint(10000, 10000000)),
            "firstname": str(random.randint(10000, 10000000)),
            "classTxt": str(random.randint(10000, 10000000)),
        },
        "related": 0,
    }
    # print(json_data)
    async with session.post(
        url=f"https://videouroki.net/tests/api/beginTest/{test_id}/",
        headers=headers,
        json=json_data,
    ) as resp:
        response = await resp.json()
        # print(response)

        member = {
            "user": json_data["member"]["lastname"]
            + " "
            + json_data["member"]["firstname"],
            "classTxt": json_data["member"]["classTxt"],
            "fakeId": response["id"],
            "uuid": response["uuid"],
        }
        return member


async def response_check(
    answers, session, headers, test_id, questions_id, questions_type
):
    member = await create_member(test_id, session, headers)
    await save_ans(
        q_id=questions_id,
        member=member,
        type=questions_type,
        variants=answers,
        session=session,
        headers=headers,
    )
    async with session.get(
        url=f'https://videouroki.net/tests/complete/{member["uuid"]}', headers=headers
    ) as resp:
        soup = BeautifulSoup(await resp.text(), features="html.parser")
        a = soup.find_all("div", class_="test_main__results_statitem")
        for i in a:
            if "Выполнено верно" in i.text:
                if i.find_all("b")[0].text == "1":
                    return True
                return False


async def get_answers_on_questions(questions, session, headers, test_id):
    res = {}
    for q in questions:
        q_text = BeautifulSoup(q["description"], features="html.parser").get_text()
        if q["type"] == 2:
            answer_options = q["answers"]
            flag = False
            for i in range(1, len(answer_options)):
                for ans in combinations(answer_options, i):
                    answers_text = [a["text"] for a in ans]
                    if await response_check(
                        answers=[a["id"] for a in ans],
                        headers=headers,
                        questions_id=q["id"],
                        questions_type=q["type"],
                        session=session,
                        test_id=test_id,
                    ):
                        res[q_text] = answers_text
                        flag = True
                        break
                if flag:
                    break
        elif q["type"] == 1:
            for ans in q["answers"]:
                answers_text = ans["text"]
                if await response_check(
                    answers=[ans["id"]],
                    headers=headers,
                    questions_id=q["id"],
                    questions_type=q["type"],
                    session=session,
                    test_id=test_id,
                ):
                    res[q_text] = answers_text
                    break

        elif q["type"] == 6:
            # Да/нет
            for s in product((1, 0), repeat=len(q["answers"])):
                ans = []
                for i, item in enumerate(q["answers"]):
                    ans.append({"answer_id": item["id"], "answer": s[i]})
                if await response_check(
                    answers=ans,
                    headers=headers,
                    questions_id=q["id"],
                    questions_type=q["type"],
                    session=session,
                    test_id=test_id,
                ):
                    res[q_text] = [
                        f"{'Нет' if s[i] == 0 else 'Да'} - {item['text'][:31].strip()}..."
                        for i, item in enumerate(q["answers"])
                    ]
                    break

        elif q["type"] == 4:
            annotation = q["annotation"]
            r = [ann["id"] for ann in json.loads(annotation)]
            for s in product(r, repeat=len(q["answers"])):
                ans = []
                for i, item in enumerate(q["answers"]):
                    ans.append({"answer_id": item["id"], "answer": s[i]})
                if await response_check(
                    answers=ans,
                    headers=headers,
                    questions_id=q["id"],
                    questions_type=q["type"],
                    session=session,
                    test_id=test_id,
                ):
                    res[q_text] = [
                        f"{s[i]} - {item['text'][:31].strip()}..."
                        for i, item in enumerate(q["answers"])
                    ]
                    break
        else:
            res[q_text] = "К сожалению,я не могу решить это задание("

    return res


async def get_test_questions(member, session, test_id):
    headers = (
        Headers(browser="chrome", os="win", headers=True)
        .generate()
        .update(
            {
                "authority": "videouroki.net",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,application/"
                "signed-exchange;v=b3;q=0.9",
                "referer": f"https://videouroki.net/tests/{test_id}/",
            }
        )
    )
    async with session.get(
        url=f'https://videouroki.net/tests/do/{member["uuid"]}', headers=headers
    ) as resp:
        response = await resp.text()
        s = response.replace("</", "<").split("<script>")
        for i in s:
            if "window.backend = " in i:
                bac = json.loads(i.replace("window.backend = ", "").strip())
                break
        questions = json.loads(bac["questions"])
        return questions


async def get_test_answer(url: str):
    async with aiohttp.ClientSession() as session:
        fake_test_url, test_title, test_page_url = await get_fake_test_url(url, session)
        logger.info(f"{fake_test_url=}, {test_title=}, {test_page_url=}")
        test_id = fake_test_url.split("/")[-2]
        header = (
            Headers(
                browser="chrome",
                os="win",
                headers=True,
            )
            .generate()
            .update(
                {
                    "Content-Type": "application/json;charset=UTF-8",
                    "Referer": url,
                }
            )
        )
        member = await create_member(test_id, session, header)
        questions = await get_test_questions(member, session, test_id)
        answers = await get_answers_on_questions(
            questions, session, header, test_id=test_id
        )
        logger.info(f"{member=}, {questions=}, {answers=}")

        res = {
            "test_title": test_title,
            "answers": answers,
            "test_page_url": test_page_url,
        }
        return res
