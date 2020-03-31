import json
import requests
import pandas as pd
from requests_futures.sessions import FuturesSession


def _get_keys(path):

    """
    blah blah blah
    """

    with open(path) as f:
        return json.load(f)


def _get_pagespeed_data(url):

    """
    blah blah blah
    """
    keys = _get_keys("/Users/sandylee/.secret/page_speed_api.json")
    api_key = keys['api_key']
    query = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}'
    request = requests.get(query, )
    response = request.json()

    try:
        address = str(response['id'].split('?')[0])
        first_contentful_paint = float(response['lighthouseResult']['audits']['first-contentful-paint']['numericValue'])
        first_interactive = float(response['lighthouseResult']['audits']['interactive']['numericValue'])
        time_to_first_byte = float(response['lighthouseResult']['audits']['time-to-first-byte']['numericValue'])
        dom_size = float(response['lighthouseResult']['audits']['dom-size']['numericValue'])
        boot_up_time = float(response['lighthouseResult']['audits']['bootup-time']['numericValue'])
        first_meaningful_paint = float(response['lighthouseResult']['audits']['first-meaningful-paint']['numericValue'])
        speed_index = float(response['lighthouseResult']['audits']['speed-index']['numericValue'])
        total_blocking_tine = float(response['lighthouseResult']['audits']['total-blocking-time']['numericValue'])
        network_requests = float(response['lighthouseResult']['audits']['network-requests']['numericValue'])
        total_byte_weight = float(response['lighthouseResult']['audits']['total-byte-weight']['numericValue'])
    except KeyError:
        print(f'<KeyError> One or more keys not found {url}/.')

    try:
        row_df = pd.DataFrame({'URL': address,
                           'First Contentful Paint': first_contentful_paint,
                           'First Interactive': first_interactive,
                           'Time to First Byte': time_to_first_byte,
                           'DOM Size': dom_size,
                           'Boot Up Time': boot_up_time,
                           'First Meaningful Paint': first_meaningful_paint,
                           'Speed Index': speed_index,
                           'Total Blocking Time': total_blocking_tine,
                           'Network Requests': network_requests,
                           'Total Byte Weight': total_byte_weight},
                          index=[0])

    except NameError:
        print(f'<NameError> Failing because of KeyError {url}.')

    return row_df


def main():
    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result
    pagespeed_results = pd.DataFrame(columns=['URL',
                                              'First Contentful Paint',
                                              'First Interactive',
                                              'Time to First Byte',
                                              'DOM Size',
                                              'Boot Up Time',
                                              'First Meaningful Paint',
                                              'Speed Index',
                                              'Total Blocking Time',
                                              'Network Requests',
                                              'Total Byte Weight'],
                                              index=[0])

    keys = _get_keys("/Users/sandylee/.secret/page_speed_api.json")
    api_key = keys['api_key']
    query = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}'

    # TODO: implement https://github.com/ross/requests-futures
    # TODO: create list of queries to feed into futures and process results


    with FuturesSession as session:
        futures = [session.get(query) for url in urls]
        for future in futures:
            future.result()
    # for url in range(0,5):
    #     result = _get_pagespeed_data(urls[url])
    #     print (result)
    #     pagespeed_results = pagespeed_results.append(result, ignore_index=True)
    # pagespeed_results = pagespeed_results.drop(index=0, axis=0)
    # pagespeed_results.to_csv('pagespeed_results.csv')

if __name__ == '__main__':
	main()