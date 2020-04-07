import pandas as pd
import requests
import os
from google.cloud import language
from concurrent.futures import as_completed, ThreadPoolExecutor


N_THREADS = 200
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sandylee/.secret/backup-142521-18d7e8c2e792.json"


def classify(url):

    try:
        text = requests.get(url).content

        language_client = language.LanguageServiceClient()
        document = language.types.Document(content=text,
                                           type=language.enums.Document.Type.HTML)
        response = language_client.classify_text(document)
        categories = response.categories
        result = {}
        for category in categories:
            result[category.name] = category.confidence

        return ([url, result])

    except Exception:
        return url


def main():
    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result[:1000]

    pool = ThreadPoolExecutor(max_workers=N_THREADS)

    try:
        futures = {pool.submit(classify, url): url for url in urls}
        for future in as_completed(futures):
            data = future.result()
            if bool(data[1]) == False:
                print(f'No API data returned for: {data[0]} ')

            elif type(data) == list:
                keys = list(data[1].keys())
                values = list(data[1].values())
                print(f'URL: {data[0]}, ',
                      f'Category: {keys[0].split("/")[1]}, ',
                      f'Confidence: {round(values[0]*100)}%')
            else:
                 print(f'Unable to retrieve page for: {data} ')

    except Exception as esc:
        print(f'An error has occurred: {esc} for {data[0]}')

#TODO: Add CSV writing to script


if __name__ == '__main__':
    main()