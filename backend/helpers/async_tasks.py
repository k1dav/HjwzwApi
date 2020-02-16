"""非同步處理"""
import asyncio
from asyncio import Queue


class AsnycHelper:
    """非同步塞入 queue 批次處理"""

    def __init__(self, max_threads: int = 5):
        self.max_threads = max_threads
        self.results = {}
        self.index = 0

    async def handle_tasks(self, task_id:int, work_queue:Queue):
        """處理任務"""
        while not work_queue.empty():
            current_url = await work_queue.get()
            try:
                task_status = await self.get_results(current_url)
            except Exception as e:
                logging.exception("Error for {}".format(current_url), exc_info=True)

    def queue_event_loop(self, list_:list):
        """建立 Queue，批次執行"""
        work_queue = Queue()
        [work_queue.put(url) for url in self.urls]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(task_id, work_queue,) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
