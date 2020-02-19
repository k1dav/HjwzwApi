"""非同步處理"""
import abc
import asyncio
from typing import List

import aiohttp
from aiohttp import ClientSession


class AsyncCrawler:
    """非同步塞入 queue 批次處理"""

    def __init__(self, max_workers: int = 5, **kwargs):
        self.max_workers = max_workers
        self.loop = asyncio.get_event_loop()
        self.q = asyncio.Queue(loop=self.loop)
        self.session = ClientSession(loop=self.loop)
        self.results = dict()

    async def crawl(self):
        """批次爬蟲任務"""
        workers = [
            asyncio.Task(self.work(), loop=self.loop) for _ in range(self.max_workers)
        ]
        await self.q.join()
        [w.cancel for w in workers]
        return self.results

    async def work(self):
        """處理任務"""
        try:
            while True:
                current_url = await self.q.get()
                print(current_url)
                resp = await self.session.get(current_url)
                self.results[current_url] = await self.fetch(resp)
                self.q.task_done()
        except asyncio.CancelledError:
            pass

    @abc.abstractmethod
    async def produce(self, **kwargs):
        """生產 Queue"""
        return NotImplemented

    @abc.abstractmethod
    async def fetch(self, resp, **kwargs):
        """執行爬蟲取得結果"""
        return NotImplemented
