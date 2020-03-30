#!/usr/bin/env python3
import asyncio
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
import csv
import json
import os
from os.path import exists
import random
from time import time

import aiohttp
import dotenv


dotenv.load_dotenv()
API_KEY = os.getenv('PAGE_SPEED_API_KEY')

COLUMNS=['URL',
        'First Contentful Paint',
        'First Interactive',
        'Time to First Byte',
        'DOM Size',
        'Boot Up Time',
        'First Meaningful Paint',
        'Speed Index',
        'Total Blocking Time',
        'Network Requests',
        'Total Byte Weight']

_pool = ProcessPoolExecutor()

PAGE_SPEED_FILE = 'page_speed.csv'
SERP_FILE = 'serp_results.csv'
MAX_CONCURRENT = 69 # number of workers processing urls


def _extract_data(url, content):
    """Return an OrderedDict populated with page speed data."""
    d = OrderedDict()
    d['URL'] = url

    audits = json.loads(content)['lighthouseResult']['audits']

    for c in COLUMNS[1:]:
        key = c.lower().replace(' ', '-')
        try:
            d[c] = audits[key]['numericValue']
        except KeyError:
            d[c] = ''

    return d


async def process_url(url, loop, session):
    query = ("https://www.googleapis.com"
            "/pagespeedonline/v5/runPagespeed"
            f"?url={url}&key={API_KEY}")
    async with session.get(query) as response:
        content = await response.read()

    return await loop.run_in_executor(_pool, _extract_data, url, content)


async def url_processor(url_q, csv_q, loop, session):
    while not url_q.empty():
        url = await url_q.get()

        try:
            d = await process_url(url, loop, session)
            await csv_q.put(d)
        except Exception as exc:
            await csv_q.put(None)
            print(f"Exception: {exc}")

        url_q.task_done()

async def csv_writer(url_q, csv_q, count):
    i, last_tenth, last_time, start_time = 0, 0, 0, time()
    print('Waiting for data.')
    while(csv_q.empty()):
        await asyncio.sleep(.1)

    append = exists(PAGE_SPEED_FILE)
    with open(PAGE_SPEED_FILE, 'a' if append else 'w') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not append:
            writer.writeheader()

        while (i < count):
            row = await csv_q.get()
            i += 1

            if not row is None:
                writer.writerow(row)
                if (10 * i // count > last_tenth
                        or time() - last_time > 3):
                    last_tenth = 10 * i // count
                    last_time = time()
                    print(f"Completed {i / count:5.2%} "
                            f"in {time() - start_time:>8.2f}s.",
                            flush=True)

            csv_q.task_done()
    print(f"Completed 100% in {time() - start_time:>6.1f}s.", flush=True)


def _seen_urls():
    with open(PAGE_SPEED_FILE) as f:
        reader = csv.reader(f)
        next(reader)
        return set(url for (url, *_) in reader)


async def main():
    url_q, csv_q = asyncio.Queue(), asyncio.Queue()
    loop = asyncio.get_running_loop()
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0))
    seen_urls = _seen_urls() if exists(PAGE_SPEED_FILE) else set()

    print("Reading SERP results")
    with open(SERP_FILE) as f:
        reader = csv.reader(f)
        next(reader)
        urls = [url for (*_, url) in reader]
    orig_len = len(urls)
    urls = list(set(urls))
    random.shuffle(urls)
    for url in urls[:144]: #TODO: unrestrict
        if url in seen_urls:
            continue
        url_q.put_nowait(url)
    print(f"Read in {orig_len} entries with {orig_len - len(urls)} "
            "duplicates found.")

    csv_task = loop.create_task(csv_writer(url_q, csv_q, url_q.qsize()))

    url_tasks = [loop.create_task(url_processor(url_q, csv_q, loop, session))
                    for _ in range(MAX_CONCURRENT)]

    await asyncio.gather(*url_tasks)
    await session.close()
    await csv_task

    print("Done!")


if __name__ == '__main__':
    asyncio.run(main())
