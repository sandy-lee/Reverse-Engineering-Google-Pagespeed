
from asyncio import get_running_loop
from collections import OrderedDict
import json
from json import JSONDecodeError
from os import getenv
from pathlib import Path

import requests
from serpapi.google_search_results import GoogleSearchResults as GSR

from .variables import N_SERP_RESULTS
from .base import get_web_content, p_pool, t_pool


try:
    import dotenv
    dotenv.load_dotenv(
        dotenv_path=Path(__file__).parent.parent / 'var' / '.env'
        )
    GSR.SERP_API_KEY = getenv('SERP_API_KEY')
    PAGE_SPEED_API_KEY = getenv('PAGE_SPEED_API_KEY')
except ImportError:
    def _key(path):
        with open(path) as f:
            return json.load(f)['api_key']

    GSR.SERP_API_KEY = _key("/Users/sandylee/.secret/serpapi.json")
    PAGE_SPEED_API_KEY = _key("/Users/sandylee/.secret/page_speed_api.json")

PAGE_SPEED_QUERY_TEMPLATE = (
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        "?url={}&key=" + PAGE_SPEED_API_KEY)


PAGE_SPEED_COLUMNS = [
    'URL',
    'First Contentful Paint',
    'First Interactive',
    'Time to First Byte',
    'DOM Size',
    'Boot Up Time',
    'First Meaningful Paint',
    'Speed Index',
    'Total Blocking Time',
    'Network Requests',
    'Total Byte Weight'
    ]
COLUMN_TO_LIGHTHOUSE = {c: c.lower().replace(' ', '-')
                        for c in PAGE_SPEED_COLUMNS}


def parse_page_speeds(url, content):
    d = OrderedDict()
    d['URL'] = url

    try:
        response = json.loads(content)
    except JSONDecodeError:
        return None

    if 'lighthouseResult' not in response:
        return None
    elif 'audits' not in response['lighthouseResult']:
        return None

    audits = response['lighthouseResult']['audits']

    for c in PAGE_SPEED_COLUMNS[1:]:
        try:
            d[c] = audits[COLUMN_TO_LIGHTHOUSE[c]]['numericValue']
        except KeyError:
            d[c] = ''

    return d


async def get_page_speed_content(url):
    query = PAGE_SPEED_QUERY_TEMPLATE.format(url)

    return await get_web_content(query)


async def get_page_speed_data(url):
    """Return an OrderedDict populated with page speed data."""
    content = await get_page_speed_content(url)

    return await get_running_loop().run_in_executor(
        p_pool, parse_page_speeds, url, content)


def parse_google_search_results(content):
    d = json.loads(content)

    return [(result["position"], result["link"])
            for result in d["organic_results"]]


async def get_serp_data(search_term):
    """Return list of (position, link) tuples containing serpapi results."""
    loop = get_running_loop()

    content = await loop.run_in_executor(
        t_pool,
        lambda query_parameters: GSR(query_parameters).get_results(),
        {
            "q": search_term,
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "num": N_SERP_RESULTS,
        })

    return await loop.run_in_executor(
        p_pool,
        parse_google_search_results, content)
