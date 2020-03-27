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
                                          'Total Byte Weight'])

for index in range(0, len(urls)):
    query = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={urls.iloc[index]}&key={api_key}'
    request = requests.get(query)
    response = request.json()
    counter += 1
    print(counter)
    try:
        urlid = response['id']
        split = urlid.split('?')  # This splits the absolute url from the api key parameter
        urlid = split[0]  # This reassigns urlid to the absolute url
        # ID = f'URL ~ {urlid}'
        # ID2 = str(urlid)
        urlfcp = response['lighthouseResult']['audits']['first-contentful-paint']['numericValue']
        # FCP = f'First Contentful Paint ~ {str(urlfcp)}'
        # FCP2 = float(urlfcp)
        urlfi = response['lighthouseResult']['audits']['interactive']['numericValue']
        # FI = f'First Interactive ~ {str(urlfi)}'
        # FI2 = float(urlfi)
        urlttfb = response['lighthouseResult']['audits']['time-to-first-byte']['numericValue']
        # TTFB = f'Time To First Byte ~ {str(urlttfb)}'
        # TTFB2 = float(urlttfb)
        urldom = response['lighthouseResult']['audits']['dom-size']['numericValue']
        # DOM  = f'DOM Size ~ {str(urldom)}'
        # DOM2 = float(urldom)
        urlboot = response['lighthouseResult']['audits']['bootup-time']['numericValue']
        # BOOT  = f'Boot Up Time ~ {str(urlboot)}'
        # BOOT2 = float(urlboot)
        urlfmp = response['lighthouseResult']['audits']['first-meaningful-paint']['numericValue']
        # FMP  = f'First Meaningful Paint ~ {str(urlfmp)}'
        # FMP2 = float(urlfmp)
        urlsi = response['lighthouseResult']['audits']['speed-index']['numericValue']
        # SI  = f'Speed Index ~ {str(urlsi)}'
        # SI2 = float(urlsi)
        urltbt = response['lighthouseResult']['audits']['total-blocking-time']['numericValue']
        # TBT  = f'Total Blocking Time ~ {str(urltbt)}'
        # TBT2 = float(urltbt)
        urlnr = response['lighthouseResult']['audits']['network-requests']['numericValue']
        # NR  = f'Network Requests ~ {str(urlnr)}'
        # NR2 = float(urlnr)
        urltbw = response['lighthouseResult']['audits']['total-byte-weight']['numericValue']
        # TBW  = f'Total Byte Weight ~ {str(urltbw)}'
        # TBW2 = float(urltbw)

    except KeyError:
        print(f'<KeyError> One or more keys not found {index}.')

    try:
        row_df = pd.DataFrame(data = [urlid,
                                      urlfcp,
                                      urlfi,
                                      urlttfb,
                                      urldom,
                                      urlboot,
                                      urlfmp,
                                      urlsi,
                                      urltbt,
                                      urlnr,
                                      urltbw])
        pagespeed_results = pd.concat(data, ignore_index = True)
#             file.write(row)
    except NameError:
        print(f'<NameError> Failing because of KeyError {index}.')
#             file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')
#
#         try:
#             print(ID)
#             print()
#             print(counter)
#             print()
#             print(FCP)
#             print(FI)
#             print(TTFB)
#             print(DOM)
#             print(BOOT)
#             print(FMP)
#             print(SI)
#             print(TBT)
#             print(NR)
#             print(TBW)
#             print()
#
#         except NameError:
#             print(f'<NameError> Failing because of KeyError {line}.')
#
#     file.close()
