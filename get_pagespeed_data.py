import json
import requests
import pandas as pd


def get_keys(path):
    with open(path) as f:
        return json.load(f)


serp_results = pd.read_csv("serp_results.csv")
urls = serp_results.result
keys = get_keys("/Users/sandylee/.secret/page_speed_api.json")
api_key = keys['api_key']
counter = 0
pagespeed_results = pd.DataFrame(columns=['url',
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

# for index in range(0, len(urls)):
for index in range(0, 5):
    query = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={urls.iloc[index]}&key={api_key}'
    request = requests.get(query)
    response = request.json()
    counter += 1
    # print(counter)
 #   try:
    url = str(response['id'].split('?'))

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


#     except KeyError:
#         print(f'<KeyError> One or more keys not found {index}.')
#
#     # try:
#
    row_df = pd.DataFrame({'url' : url,
                           'First Contentful Paint' : first_contentful_paint,
                           'First Interactive' : first_interactive,
                           'Time to First Byte' : time_to_first_byte,
                           'DOM Size' : dom_size,
                           'Boot Up Time' : boot_up_time,
                           'First Meaningful Paint' : first_meaningful_paint,
                           'Speed Index' : speed_index,
                           'Total Blocking Time' : total_blocking_tine,
                           'Network Requests' : network_requests,
                           'Total Byte Weight' : total_byte_weight},
                           index=[0])

    pagespeed_results = pagespeed_results.append(row_df,ignore_index=True)

pagespeed_results.to_csv('pagespeed_results')
#
#
#     print(row_df)
# #             file.write(row)
# #     except NameError:
# #         print(f'<NameError> Failing because of KeyError {index}.')
# #             file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')
# #
# #         try:
# #             print(ID)
# #             print()
# #             print(counter)
# #             print()
# #             print(FCP)
# #             print(FI)
# #             print(TTFB)
# #             print(DOM)
# #             print(BOOT)
# #             print(FMP)
# #             print(SI)
# #             print(TBT)
# #             print(NR)
# #             print(TBW)
# #             print()
# #
# #         except NameError:
# #             print(f'<NameError> Failing because of KeyError {line}.')
# #
# #     file.close()