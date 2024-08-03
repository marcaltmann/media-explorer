from datetime import datetime, timedelta

from django.http import QueryDict
from django.utils.translation import gettext_lazy as _


class Document:
    """One Solr document/search result."""
    pass


class ResourceDocument(Document):
    """Solr Resource document."""
    def __init__(self, doc: dict) -> None:
        self.id = int(doc['id'])
        self.title = doc['title_t']
        self.description = doc.get('description_t', "")
        self.media_type = doc['media_type_s']
        self.media_files_count = doc['media_files_count_i']
        self.duration = timedelta(seconds=doc['duration_i'])
        self.production_date = datetime.fromisoformat(doc['production_date_dt']).date()
        self.public = doc['public_b']
        #self.transcript = doc['transcript_t']
        self.version = doc['_version_']
        self.score = doc['score']


class SearchResults:
    """
    Initialized with the Solr search results.
    """
    def __init__(self, results: dict) -> None:
        self.header = results["responseHeader"]
        self.debug = results.get("debug")
        response = results["response"]
        self.num_found = response["numFound"]
        self.start = response["start"]
        self.max_score = response["maxScore"]
        self.docs = [ResourceDocument(doc) for doc in response["docs"]]
        self.page_len = len(self.docs)

        self.original_facets = results["facet_counts"]["facet_fields"]
        self.original_ranges = results["facet_counts"]["facet_ranges"]
        self.facets = transform_facets(self.original_facets)
        self.ranges = transform_ranges(self.original_ranges)


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
