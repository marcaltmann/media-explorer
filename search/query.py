import requests

from search.facets import FacetGroup
from search.results import SearchResults

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
    results = SearchResults(response.json())

    return results
