import pandas as pd
import requests
from google.cloud import language

def get_html(url):
    return (requests.get(url))


def classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.HTML)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))

    return result

def main():

    serp_results = pd.read_csv("serp_results.csv")
    urls = serp_results.result[:1]

    for url in urls:
        webpage = get_html(url)
        classify(webpage)


if __name__ == '__main__':
    main()