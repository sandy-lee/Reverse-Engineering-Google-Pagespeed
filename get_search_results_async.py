#!/usr/bin/env python3
from concurrent.futures import as_completed, ThreadPoolExecutor
import csv
import os
import sys

import dotenv
from serpapi.google_search_results import GoogleSearchResults

dotenv.load_dotenv()
GoogleSearchResults.SERP_API_KEY = os.getenv('SERP_API_KEY')

N_THREADS = 100 # no. of concurrent serpapi requests
N_RESULTS = 100 # no. of results for each keyword


def top_results(keyword):
    """Return list of (position, link) tuples for keyword results."""
    query_parameters = {"q": keyword,
                        "hl": "en",
                        "gl": "us",
                        "google_domain": "google.com",
                        "num": N_RESULTS,
                        }
    response = GoogleSearchResults(query_parameters).get_dict()

    return [(result["position"], result["link"])
                for result in response["organic_results"]]


def main():
    print('Reading search terms')
    with open("top_1000_search_terms.csv") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        keywords = [kwd for (kwd,) in reader]

    pool = ThreadPoolExecutor(max_workers=N_THREADS)

    future_to_kwd = {pool.submit(top_results, kwd): kwd
                        for kwd in keywords[:5]} #TODO: unrestrict

    with open('herp_derp_results.csv', 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["keyword", "position", "result"])

        i = 0
        for future in as_completed(future_to_kwd):
            kwd = future_to_kwd[future]
            try:
                results = future.result()
                csvwriter.writerows([(kwd, pos, lnk)
                                        for (pos, lnk) in results])
                i += 1
                print(f"\rCompleted {i/len(future_to_kwd):.1%}", end='')
                sys.stdout.flush()
            except Exception as exc:
                print(f'\n\nException: {exc}\n')
    print('\nDone')

if __name__ == '__main__':
    main()
