import pandas as pd
import json
import csv
from requests_futures.sessions import FuturesSession

def _get_keys(path):
    with open(path) as f:
        return json.load(f)  # TODO: pipenv install python-dotenv


def _parse_result(future_obj):
    # I've noticed pagespeedonline sometimes returning
    # malformed JSON documents.
    # probably want a try/except for json.JSONDecodeError
    response = json.loads(future_obj.result().content.decode('utf-8'))
    url = None
    first_contentful_paint = None
    first_interactive = None
    time_to_first_byte = None
    dom_size = None
    boot_up_time = None
    first_meaningful_paint = None
    speed_index = None
    total_blocking_time = None
    network_requests = None
    total_byte_weight = None

    try:
        url = str(response.get('id', "").split('?')[0])
        #  why convert to float then back to str for CSV file?
        first_contentful_paint = float(response.get('lighthouseResult').get('audits')
                                       .get('first-contentful-paint').get('numericValue'))
        first_interactive = float(response.get('lighthouseResult').get('audits')
                                  .get('interactive').get('numericValue'))
        time_to_first_byte = float(response.get('lighthouseResult').get('audits')
                                   .get('time-to-first-byte').get('numericValue'))
        dom_size = float(response.get('lighthouseResult').get('audits').get('dom-size')
                         .get('numericValue'))
        boot_up_time = float(response.get('lighthouseResult').get('audits')
                             .get('bootup-time').get('numericValue'))
        first_meaningful_paint = float(response.get('lighthouseResult').get('audits')
                                       .get('first-meaningful-paint').get('numericValue'))
        speed_index = float(response.get('lighthouseResult').get('audits')
                            .get('speed-index').get('numericValue'))
        total_blocking_time = float(response.get('lighthouseResult').get('audits')
                                    .get('total-blocking-time').get('numericValue'))
        network_requests = float(response.get('lighthouseResult').get('audits')
                                 .get('network-requests').get('numericValue'))
        total_byte_weight = float(response.get('lighthouseResult').get('audits')
                                  .get('total-byte-weight').get('numericValue'))
    except Exception as esc:
        print(f'An error has occurred: {esc}')
        with open('pagespeed_results.csv', 'a') as f:
            csvwriter = csv.writer(f)
            f.write(f'MISSING URL: {future_obj.result().url}')

    finally:
        row = [url,
               first_contentful_paint,
               first_interactive,
               time_to_first_byte,
               dom_size,
               boot_up_time,
               first_meaningful_paint,
               speed_index,
               total_blocking_time,
               network_requests,
               total_byte_weight]

        with open('pagespeed_results.csv', 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(row)


def main():

    keys = _get_keys("/Users/sandylee/.secret/page_speed_api.json")
    api_key = keys['api_key']  # just a coincidence that the name of the
                               # CCP virus is an anagram of carnivorous?!

    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result[:10]

    with open('pagespeed_results.csv', 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["URL",
                            "FCP",
                            "FI",
                            "TTFB",
                            "DOM",
                            "BUT",
                            "FMP",
                            "SI",
                            "TBT",
                            "NR",
                            "TBW"])

    with FuturesSession() as session:
        futures = [session
                   .get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}')
                   # get_pagespeed_data_async.py:96:80: PEP8 checker error:
                   # E501 line too long (110 > 79 characters)
                   for url in urls]
        # I think the callbacks are also done in the thread context that was
        # processing the request.
        # https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.add_done_callback
        # If you have multiple threads writing the same file
        # you're going to have a bad time.
        # Easily fixed, anyway :)
        # https://github.com/ross/requests-futures#iterating-over-a-list-of-requests-responses
        # so long as you don't mind them being unordered...
        # 
        # from concurrent.futures import as_completed
        # for future in as_completed(futures):
        #     _parse_result(future)
        for future in futures:
            future.add_done_callback(_parse_result)


if __name__ == '__main__':
    main()
