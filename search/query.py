import requests

from search.facets import FacetGroup

SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def query_resource(query: str, facet_group: FacetGroup):
    query = query or "*"
    facets = facet_group.solr_query()

    url = SOLR_URL + (
        f"select?defType=edismax&q={query}"
        "&qf=title_t description_t transcript_t media_type_s"
        "&fl=*,score&wt=json&debug=all&" + facets
    )

    response = requests.get(url)
    result = response.json()

    docs = result["response"]["docs"]
    count = result["response"]["numFound"]
    facets = result["facet_counts"]["facet_fields"]
    ranges = result["facet_counts"]["facet_ranges"]

    return docs, count, transform_facets(facets), transform_ranges(ranges)


def transform_facets(facets):
    result = dict()
    for facet in facets:
        values = facets[facet]
        result[facet] = transform_facet_values(values)
    return result


def transform_ranges(facets):
    result = dict()
    for facet in facets:
        values = facets[facet]["counts"]
        result[facet] = {
            "counts": transform_facet_values(values),
            "gap": facets[facet]["gap"],
            "start": facets[facet]["start"],
            "end": facets[facet]["end"],
        }
    return result


def transform_facet_values(facet_values):
    result = dict()
    it = iter(facet_values)
    for value in it:
        count = next(it)
        result[value] = count
    return result
