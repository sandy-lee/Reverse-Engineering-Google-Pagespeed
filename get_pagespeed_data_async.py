from requests_futures.sessions import FuturesSession
import pandas as pd
import json


def get_keys(path):
    with open(path) as f:
        return json.load(f)

def main():


    keys = get_keys("/Users/sandylee/.secret/page_speed_api.json")
    api_key = keys['api_key']

    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result[:5]

    def print_result(future_obj):
        response = future_obj.result()
        print(response.url)

    with FuturesSession() as session:
        futures = [session.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}') for url in urls]
        for future in futures:

            future.add_done_callback(print_result)



if __name__ == '__main__':
	main()