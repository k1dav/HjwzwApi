"""黃金屋的爬蟲"""
import asyncio
import re
from typing import List

import aiohttp
import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from backend.helpers.async_tasks import AsyncCrawler
from backend.schemas.search import Book

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


class Chapters(AsyncCrawler):
    """取得章節資料"""

    url_template = MOBILE_URL + "/ChapterList/{book_id}/{start}_{end}"
    range = 300  # 一次 query 數量
    start = 0
    end = range
    length = 0  # 總章節數

    def __init__(self, max_workers: int = 3, **kwargs):
        super().__init__(max_workers, **kwargs)

        self.start = kwargs.get("start", self.start)
        self.end = kwargs.get("end", self.end)
        self.range = kwargs.get("range", self.range)
        self.book_id = kwargs["book_id"]

        self.__set_length()
        for _ in range(max_workers * 2):
            self.produce()

    def produce(self, **kwargs):
        """生產 url"""
        if self.start == self.length:
            # 終止
            return

        if self.end > self.length:
            # 調整最後一筆
            self.end = self.length

        self.q.put_nowait(
            self.url_template.format(
                book_id=self.book_id, start=self.start, end=self.end
            )
        )
        self.start = self.end
        self.end = self.end + self.range

    async def fetch(self, resp, **kwargs):
        """取得章節資料"""
        assert resp.status == 200

        text = await resp.text()
        soup = BeautifulSoup(text, "html.parser")

        chapters = soup.select("a[title^='第']")
        if len(chapters) == 0:
            return None
        elif len(chapters) == self.range:
            self.produce(**kwargs)

        list_ = list()
        for chapter in chapters:
            list_.append(
                {
                    "chapter_id": chapter["href"].replace("/Read/", ""),
                    "title": chapter["title"].strip(),
                }
            )
        return list_

    def __set_length(self):
        """設定長度，超過會取不到資料"""
        resp = requests.get(f"https://t.hjwzw.com/Chapter/{self.book_id}")
        assert resp.status_code == 200

        soup = BeautifulSoup(resp.text, "html.parser")
        chapter_lists = soup.select("a[title^='第']")
        self.length = int(chapter_lists[-1]["href"].split("_")[-1])
