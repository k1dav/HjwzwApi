"""黃金屋的爬蟲"""
import asyncio
import re

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from backend.schemas.search import Book
from typing import List

BASE_URL = "https://tw.hjwzw.com"
MOBILE_URL = "https://t.hjwzw.com"


async def search_title(title: str) -> List[Book]:
    """取得搜尋資料"""
    url = f"{BASE_URL}/List/{title}"

    async with ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            text = await resp.text()

            soup = BeautifulSoup(text, "html.parser")

            # 是直接搜到書本主頁嗎
            main = soup.find_all("a", string=re.compile(f"{title}"))
            is_main = main != None and all([main[0]["href"] in i["href"] for i in main])

            if is_main:
                main = main[0]
                list_ = [await get_book_info(main.text.strip(), main["href"])]
            else:
                books = soup.find_all("span", class_="wd10")
                list_ = await asyncio.gather(
                    *[get_book_info(i.a.text, i.a["href"]) for i in books]
                )
            return list_


async def get_book_info(title: str, url: str) -> Book:
    """取得書本資料"""
    url = f"{MOBILE_URL}{url}"

    async with ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200

            text = await resp.text()
            soup = BeautifulSoup(text, "html.parser")

            return Book(
                **{
                    "title": title,
                    "author": soup.find("span", string="作者：")
                    .findNext("span")
                    .text.strip(),
                    "preface": soup.find("div", id="Contents")
                    .text.strip()
                    .replace("\r", "")
                    .replace("\n", ""),
                    "book_id": url.split("/")[-1],
                }
            )


# TODO: asyncgrab
async def get_chapters_list(book_id: str, start: int = 0, range: int = 100) -> list:
    """取得章節資料"""
    end = range
    url = f"{MOBILE_URL}/ChapterList/{book_id}/{start}_{end}"

    async with ClientSession() as session:
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.urls]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(task_id, q,) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


async def get_chapters(session: ClientSession, url: str):
    """取得章節列表"""
    async with session.get(url) as resp:
        assert resp.status == 200

        text = await resp.text()
        soup = BeautifulSoup(text, "html.parser")

        chapters = soup.find_all("div", class_="book_list_03")

        if len(chapters) != (end - start):
            return

        list_ = []
        for chapter in chapters:
            list_.append({"title": chapter.text.strip()})

        return list_
