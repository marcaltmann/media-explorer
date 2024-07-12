import requests


SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def query_resource(query):
    url = SOLR_URL + f'select?q=title_s:{query}&df=title_s&wt=json'
    response = requests.get(url)
    result = response.json()
    print(result)
    docs = result['response']['docs']
    count = result['response']['numFound']
    return docs, count
