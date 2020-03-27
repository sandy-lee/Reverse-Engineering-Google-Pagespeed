import requests

# Documentation: https://developers.google.com/speed/docs/insights/v5/get-started

# JSON paths: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed

# Populate 'pagespeed.txt' file with URLs to query against API.
counter = 0

with open('pagespeed.txt') as pagespeedurls:
    download_dir = 'pagespeed-results.csv'
    file = open(download_dir, 'w')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]

    columnTitleRow = "URL, First Contentful Paint (ms), First Interactive (ms), Time To First Byte (ms), DOM Size (elements), Boot Up Time (ms), First Meaningful Paint (ms), Speed Index (ms), Total Blocking Time (ms), Network Requests (elements), Total Byte Weight (bytes)\n"
    file.write(columnTitleRow)

    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file
    for line in content:
        # If no "strategy" parameter is included, the query by default returns desktop data.
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}'
        print(f'Requesting {x}...')
        print()
        r = requests.get(x)
        final = r.json()
        counter +=1
        try:
            urlid = final['id']
            split = urlid.split('?') # This splits the absolute url from the api key parameter
            urlid = split[0] # This reassigns urlid to the absolute url
            ID = f'URL ~ {urlid}'
            ID2 = str(urlid)
            urlfcp = final['lighthouseResult']['audits']['first-contentful-paint']['numericValue']
            FCP = f'First Contentful Paint ~ {str(urlfcp)}'
            FCP2 = float(urlfcp)
            urlfi = final['lighthouseResult']['audits']['interactive']['numericValue']
            FI = f'First Interactive ~ {str(urlfi)}'
            FI2 = float(urlfi)
            urlttfb = final['lighthouseResult']['audits']['time-to-first-byte']['numericValue']
            TTFB = f'Time To First Byte ~ {str(urlttfb)}'
            TTFB2 = float(urlttfb)
            urldom = final['lighthouseResult']['audits']['dom-size']['numericValue']
            DOM  = f'DOM Size ~ {str(urldom)}'
            DOM2 = float(urldom)
            urlboot = final['lighthouseResult']['audits']['bootup-time']['numericValue']
            BOOT  = f'Boot Up Time ~ {str(urlboot)}'
            BOOT2 = float(urlboot)
            urlfmp = final['lighthouseResult']['audits']['first-meaningful-paint']['numericValue']
            FMP  = f'First Meaningful Paint ~ {str(urlfmp)}'
            FMP2 = float(urlfmp)
            urlsi = final['lighthouseResult']['audits']['speed-index']['numericValue']
            SI  = f'Speed Index ~ {str(urlsi)}'
            SI2 = float(urlsi)
            urltbt = final['lighthouseResult']['audits']['total-blocking-time']['numericValue']
            TBT  = f'Total Blocking Time ~ {str(urltbt)}'
            TBT2 = float(urltbt)
            urlnr = final['lighthouseResult']['audits']['network-requests']['numericValue']
            NR  = f'Network Requests ~ {str(urlnr)}'
            NR2 = float(urlnr)
            urltbw = final['lighthouseResult']['audits']['total-byte-weight']['numericValue']
            TBW  = f'Total Byte Weight ~ {str(urltbw)}'
            TBW2 = float(urltbw)
            
        except KeyError:
            print(f'<KeyError> One or more keys not found {line}.')
        
        try:
            row = f'{ID2},{FCP2},{FI2},{TTFB2},{DOM2},{BOOT2},{FMP2},{SI2},{TBT2},{NR2},{TBW2}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')
        
        try:
            print(ID) 
            print()
            print(counter)
            print()
            print(FCP)
            print(FI)
            print(TTFB)
            print(DOM)
            print(BOOT)
            print(FMP)
            print(SI)
            print(TBT)
            print(NR)
            print(TBW)
            print()
            
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')

    file.close()
