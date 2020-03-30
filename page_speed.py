#!/usr/bin/env python3
import asyncio
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor
import csv
import json
import os

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


async def process_url(url, loop):
    #TODO: aiohttp
    import requests
    query = ("https://www.googleapis.com"
            "/pagespeedonline/v5/runPagespeed"
            f"?url={url}&key={API_KEY}")
    request = requests.get(query,)

    print(_extract_data(url, request.content))


async def url_processor(url_q, csv_q, loop):
    pass


async def csv_writer(url_q, csv_q):
    pass


async def main():
    url_q, csv_q = asyncio.Queue(), asyncio.Queue()
    loop = asyncio.get_running_loop()

    print("Reading SERP results")
    with open('serp_results.csv') as f:
        reader = csv.reader(f)
        next(reader)
        urls = [url for (*_, url) in reader]
    orig_len = len(urls)
    urls = list(set(urls))
    for url in urls:
        url_q.put_nowait(url)
    print(f"Read in {orig_len} entries with {orig_len - len(urls)} "
            "duplicates found.")
    print(urls[:10])


if __name__ == '__main__':
    asyncio.run(main())
