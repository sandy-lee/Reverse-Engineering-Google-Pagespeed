import pandas as pd
import requests
import os
from google.cloud import language


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sandylee/.secret/backup-142521-18d7e8c2e792.json"


def get_html(url):
    return requests.get(url)


def classify(text, verbose=True):

    """Classify input text into categories. """

    language_client = language.LanguageServiceClient()
    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.HTML)
    response = language_client.classify_text(document)
    categories = response.categories
    result = {}
    for category in categories:
        result[category.name] = category.confidence

    return result


def main():

    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result[10:15]
    for url in urls:
        webpage = get_html(url)
        classification = classify(webpage.text)
        data = list(classification.items())
        print(url)
        print('='* len(url))
        print(f'Primary Category: {data[0][0].split("/")[1]}')
        print(f'Secondary Category: {data[0][0].split("/")[2]}')
        print(f'Confidence: {round(data[0][1] * 100)}%')




if __name__ == '__main__':
    main()