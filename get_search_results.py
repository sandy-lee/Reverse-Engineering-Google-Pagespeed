from serpapi.google_search_results import GoogleSearchResults
import pandas as pd
import json


def get_keys(path):
    with open(path) as f:
        return json.load(f)


keys = get_keys("/Users/sandylee/.secret/serpapi.json")
GoogleSearchResults.SERP_API_KEY = keys['api_key']

search_terms_df = pd.read_csv('top_1000_search_terms.csv')
result_df = pd.DataFrame(columns=["keyword", "position", "result"])

for index in range(0, len(search_terms_df)):

    keyword = (search_terms_df.iloc[index, 0])
    query_parameters = {"q": keyword,
                        "hl": "en",
                        "gl": "us",
                        "google_domain": "google.com",
                        "num": 100
                        }
    request = GoogleSearchResults(query_parameters)
    response = request.get_dict()

    for i in range(0, len(response["organic_results"])):

        position = response["organic_results"][i]["position"]
        result = response["organic_results"][i]["link"]
        result_df.loc[i + len(result_df)] = [keyword, position, result]

result_df.to_csv("serp_results.csv")
