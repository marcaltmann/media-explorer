import requests


SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def query_resource(query):
    query = query or "*"
    url = SOLR_URL + f"select?defType=edismax&q={query}&qf=title_t description_t media_type_s&wt=json"
    response = requests.get(url)
    result = response.json()
    docs = result["response"]["docs"]
    count = result["response"]["numFound"]
    return docs, count
