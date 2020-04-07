import pandas as pd
import requests
import os
from google.cloud import language
from concurrent.futures import as_completed, ThreadPoolExecutor


N_THREADS = 100
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sandylee/.secret/backup-142521-18d7e8c2e792.json"



def classify(url):

    """Classify input text into categories. """

    text = requests.get(url).content

    language_client = language.LanguageServiceClient()
    document = language.types.Document(content=text,
                                       type=language.enums.Document.Type.HTML)
    response = language_client.classify_text(document)
    categories = response.categories
    result = {}
    for category in categories:
        result[category.name] = category.confidence

    # data = list(result.items())
    # print(url)
    # print('=' * len(url))
    # print(f'Primary Category: {data[0][0].split("/")[1]}')
    # print(f'Secondary Category: {data[0][0].split("/")[2]}')
    # print(f'Confidence: {round(data[0][1] * 100)}%')

    return result


def main():
    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result

    pool = ThreadPoolExecutor(max_workers=N_THREADS)

    futures = {pool.submit(classify, url): url for url in urls[:5]}
    for future in as_completed(futures):

        print(future.result())



    # for url in urls:
    #     webpage = get_html(url)
    #     classification = classify(url, webpage.text)





if __name__ == '__main__':
    main()