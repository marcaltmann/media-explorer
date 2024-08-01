import requests


SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def query_resource(query):
    query = query or "*"
    url = SOLR_URL + (
        f"select?defType=edismax&q={query}"
        "&qf=title_t description_t transcript_t media_type_s"
        "&fl=*,score&wt=json"
        "&facet=true&facet.mincount=1&facet.field=media_type_s"
        "&debug=all"
    )
    response = requests.get(url)
    result = response.json()

    docs = result["response"]["docs"]
    count = result["response"]["numFound"]
    facets = result["facet_counts"]["facet_fields"]

    return docs, count, transform_facets(facets)


def transform_facets(facets):
    result = dict()
    for facet in facets:
        values = facets[facet]
        result[facet] = transform_facet_values(values)
    return result


def transform_facet_values(facet_values):
    result = dict()
    it = iter(facet_values)
    for value in it:
        count = next(it)
        result[value] = count
    return result
