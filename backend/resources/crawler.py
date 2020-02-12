"""黃金屋的爬蟲"""
import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://tw.hjwzw.com"
MOBILE_URL = "https://t.hjwzw.com"


async def get_book_info(title: str, url: str) -> dict:
    """取得書本資料"""
    url = f"{MOBILE_URL}{url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200

            text = await resp.text()
            soup = BeautifulSoup(text, "html.parser")

            return {
                "title": title,
                "author": soup.find("span", string="作者：").findNext("span").text.strip(),
                "preface": soup.find("div", id="Contents")
                .text.strip()
                .replace("\r", "")
                .replace("\n", ""),
                "book_id": url.split("/")[-1],
            }


async def search_title(title: str) -> list:
    """取得搜尋資料"""
    url = f"{BASE_URL}/List/{title}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            text = await resp.text()

            soup = BeautifulSoup(text, "html.parser")

            # 是直接搜到書本主頁嗎
            main = soup.find_all("a", string=re.compile(f"{title}"))
            is_main = main != None and all([main[0]["href"] in i["href"] for i in main])

            if is_main:
                main = main[0]
                list_ = await get_book_info(main.text.strip(), main["href"])
            else:
                books = soup.find_all("span", class_="wd10")
                list_ = await asyncio.gather(
                    *[get_book_info(i.a.text, i.a["href"]) for i in books]
                )
            return list_
