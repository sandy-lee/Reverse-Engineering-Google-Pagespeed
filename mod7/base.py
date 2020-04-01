
from asyncio import get_running_loop
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from aiohttp import ClientSession, TCPConnector

from .variables import N_IO_WORKERS


aiohttp_session = ClientSession(connector=TCPConnector(limit=N_IO_WORKERS))
p_pool = ProcessPoolExecutor()
t_pool = ThreadPoolExecutor(max_workers=N_IO_WORKERS)


async def get_web_content(url):
    async with aiohttp_session.get(url) as response:
        return await response.read()


class Metric:
    columns = []

    def __init__(self):
        self.loop = get_running_loop()

    def _new_row(self, url):
        row = OrderedDict()
        for c in self.columns:
            row[c] = ''
        return row

    async def process(self, url, content):
        pass

    async def run_in_process(self, func, *args):
        return await self.loop.run_in_executor(p_pool, func, *args)

    async def run_in_thread(self, func, *args):
        return await self.loop.run_in_executor(t_pool, func, *args)
