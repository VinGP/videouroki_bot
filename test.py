import asyncio
import json
import random
from pprint import pprint
from bs4 import BeautifulSoup
from itertools import combinations
from fake_headers import Headers
import requests
import aiohttp


async def get_fake_test_url(url):
    headers = Headers(browser="chrome", os="win", headers=True).generate().update({'authority': 'videouroki.net', })
    soup = BeautifulSoup(
        requests.get(url=url, headers=headers).text,
        features="html.parser")
    test_title = soup.find("p", class_="test_header__ui_testname").get_text()
    del soup
    headers = {
        'authority': 'cse.google.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': '1P_JAR=2023-01-27-05; NID=511=d3N6RP81mcA_JwyIAAFNg0wzxJwboOHETEDjLmeZOEZdpc21FtojaMLUXjbvyC-ObIYWWHLcBxU45PZcrdMv2e_Fdv9sE5RN0_WoTrnPkPxPjAjRfKgbQmPb5oVCtG11KGwxMC44TYNgXEGDXgnUgawi4-qf0_yo7p5shUPCSBqFDxPQP75Tp0iE2sdn8AXVEzKmzUDHOZdbnoQ9xSbS8l8uUMCLGDHa',
        'pragma': 'no-cache',
        'referer': 'https://videouroki.net/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-client-data': 'CIq2yQEIpbbJAQjEtskBCKmdygEIqe3KAQiTocsBCLWGzQEI9ojNAQjXjM0B',
    }

    # cookies = {
    #     '1P_JAR': '2023-01-27-05',
    #     'NID': '511=d3N6RP81mcA_JwyIAAFNg0wzxJwboOHETEDjLmeZOEZdpc21FtojaMLUXjbvyC-ObIYWWHLcBxU45PZcrdMv2e_Fdv9sE5RN0_WoTrnPkPxPjAjRfKgbQmPb5oVCtG11KGwxMC44TYNgXEGDXgnUgawi4-qf0_yo7p5shUPCSBqFDxPQP75Tp0iE2sdn8AXVEzKmzUDHOZdbnoQ9xSbS8l8uUMCLGDHa',
    # }

    response = requests.get(
        f'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=ru&source=gcsc&gss=.com&cselibv=c20e9fb0a344f1f9&cx=002726216306166405977:gcagx71gt_c&q={test_title}&safe=off&cse_tok=ALwrddHJmfJF5mP-4xx0Kl38mgX7:1674799158435&sort=&exp=csqr,cc&callback=google.search.cse.api18418',
        headers=headers,
        # cookies=cookies,
    )
    search_res = response.text.replace("/*O_o*/\ngoogle.search.cse.api18418(", "")[:-2]
    search_res = json.loads(search_res)
    p = search_res["results"][0]["url"]
    del search_res
    print(p)
    fake_test_url = \
        BeautifulSoup(requests.get(p).text, features="html.parser").find("a", class_="btn blue",
                                                                         attrs={"rel": "nofollow"})[
            "href"]
    fake_test_url = "https://videouroki.net" + fake_test_url
    return fake_test_url


async def main():
    await get_fake_test_url("https://videouroki.net/tests/3053302/")


if __name__ == '__main__':
    asyncio.run(main())

    # print(get_fake_test_url("https://videouroki.net/tests/3053302/"))
