from serpapi.google_search_results import GoogleSearchResults
import pandas as pd
import json


import pandas as pd
import json
import csv
from requests_futures.sessions import FuturesSession


def get_keys(path):
    with open(path) as f:
        return json.load(f)


keys = get_keys("/Users/sandylee/.secret/serpapi.json")
GoogleSearchResults.SERP_API_KEY = keys['api_key']