import json
import random
from pprint import pprint
from bs4 import BeautifulSoup
from itertools import combinations

import requests

headers = {
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://videouroki.net/tests/3053302/',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'member': {
        'id': False,
        'lastname': '123',
        'firstname': '123',
        'classTxt': '123',
    },
    'related': 0,
}

response = requests.post('https://videouroki.net/tests/api/beginTest/3053302/', headers=headers, json=json_data)

pprint(response.json())

print(response.json()["uuid"])

import requests

cookies = {
    '_ym_uid': '1638801073929278616',
    '_ym_d': '1665467029',
    'PHPSESSID': 'kcgjj76sop86j0ug12d7fklfq4',
    '_ym_isad': '1',
    '_ga': 'GA1.2.1457463228.1674745625',
    '_gid': 'GA1.2.1315634181.1674745625',
    '_ym_visorc': 'b',
    '__gsas': 'ID=896e2c672b0093d3:T=1674758872:S=ALNI_MZSrFDrMFhOQR3sqfODLyah6N3jUg',
    '_gat_UA-5917091-1': '1',
}

headers = {
    'authority': 'videouroki.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': '_ym_uid=1638801073929278616; _ym_d=1665467029; PHPSESSID=kcgjj76sop86j0ug12d7fklfq4; _ym_isad=1; _ga=GA1.2.1457463228.1674745625; _gid=GA1.2.1315634181.1674745625; _ym_visorc=b; __gsas=ID=896e2c672b0093d3:T=1674758872:S=ALNI_MZSrFDrMFhOQR3sqfODLyah6N3jUg; _gat_UA-5917091-1=1',
    'pragma': 'no-cache',
    'referer': 'https://videouroki.net/tests/3053302/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

response = requests.get(
    f'https://videouroki.net/tests/do/{response.json()["uuid"]}',
    cookies=cookies,
    headers=headers,
)

s = response.text.replace("</", "<").split("<script>")
for i in s:
    if "window.backend = " in i:
        # print(i)
        bac = json.loads(i.replace("window.backend = ", "").strip())
        break
q_all = json.loads(bac["questions"])

pprint(q_all)


def save_ans(q_id, type, member, variants):
    import requests

    cookies = {
        '_ym_uid': '1638801073929278616',
        '_ym_d': '1665467029',
        'PHPSESSID': 'kcgjj76sop86j0ug12d7fklfq4',
        '_ym_isad': '1',
        '_ga': 'GA1.2.1457463228.1674745625',
        '_gid': 'GA1.2.1315634181.1674745625',
        '_ym_visorc': 'b',
        '__gsas': 'ID=896e2c672b0093d3:T=1674758872:S=ALNI_MZSrFDrMFhOQR3sqfODLyah6N3jUg',
        '_gat_UA-5917091-1': '1',
    }

    headers = {
        'authority': 'videouroki.net',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': '_ym_uid=1638801073929278616; _ym_d=1665467029; PHPSESSID=kcgjj76sop86j0ug12d7fklfq4; _ym_isad=1; _ga=GA1.2.1457463228.1674745625; _gid=GA1.2.1315634181.1674745625; _ym_visorc=b; __gsas=ID=896e2c672b0093d3:T=1674758872:S=ALNI_MZSrFDrMFhOQR3sqfODLyah6N3jUg; _gat_UA-5917091-1=1',
        'origin': 'https://videouroki.net',
        'referer': f'https://videouroki.net/tests/do/{member["uuid"]}',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'answer': {
            'id': q_id,
            'variants': variants[0] if type == 1 else variants,
        },
        'member': member
    }
    # print(json_data)
    response = requests.post(f'https://videouroki.net/tests/api/save/{member["fakeId"]}/', cookies=cookies,
                             headers=headers,
                             json=json_data)
    # print("!!!", response.text)


def create_member():
    json_data = {
        'member': {
            'id': False,
            'lastname': str(random.randint(10000, 10000000)),
            'firstname': str(random.randint(10000, 10000000)),
            'classTxt': str(random.randint(10000, 10000000)),
        },
        'related': 0,
    }
    response = requests.post('https://videouroki.net/tests/api/beginTest/3053302/', headers=headers,
                             json=json_data).json()

    member = {
        'user': json_data['member']['lastname'] + ' ' + json_data['member']['firstname'],
        'classTxt': json_data['member']['classTxt'],
        'fakeId': response['id'],
        'uuid': response['uuid']
    }
    return member


dc = {}
print(len(q_all))
for q in q_all:
    # print(q)
    # print(dc)
    # print(BeautifulSoup(q['description'], features="html.parser").get_text())
    description = BeautifulSoup(q['description'], features="html.parser").get_text()
    if q['type'] == 2:
        ans = q["answers"]
        # dc[q['description']] = None
        flag = False
        for i in range(1, len(ans)):
            for n in combinations(ans, i):
                text = [s['text'] for s in n]
                member = create_member()
                save_ans(member=member, q_id=q['id'], type=q['type'], variants=[a['id'] for a in n])
                res = requests.get(
                    f'https://videouroki.net/tests/complete/{member["uuid"]}',
                    cookies=cookies,
                    headers=headers,
                )
                soup = BeautifulSoup(res.text, features="html.parser")
                a = soup.find_all("div", class_="test_main__results_statitem")
                for i in a:
                    if "Выполнено верно" in i.text:
                        if i.find_all('b')[0].text == "1":
                            dc[description] = text
                            flag = True
                            break
                if flag:
                    break
            if flag:
                break
    else:
        for ans in q['answers']:
            # break
            text = ans['text']
            member = create_member()
            save_ans(member=member, q_id=q['id'], type=q['type'], variants=[ans['id']])
            res = requests.get(
                f'https://videouroki.net/tests/complete/{member["uuid"]}',
                cookies=cookies,
                headers=headers,
            )
            soup = BeautifulSoup(res.text, features="html.parser")
            a = soup.find_all("div", class_="test_main__results_statitem")
            for i in a:
                if "Выполнено верно" in i.text:
                    if i.find_all('b')[0].text == "1":
                        dc[description] = text
                        # print("!!!", dc)
                        break
            else:
                continue
            break

pprint(dc)
