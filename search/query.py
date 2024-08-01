import requests


SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def query_resource(query):
    query = query or "*"
    url = SOLR_URL + (
        f"select?defType=edismax&q={query}"
        "&qf=title_t description_t transcript_t media_type_s"
        "&fl=*,score&wt=json"
        "&facet=true&facet.mincount=1"
        "&facet.field=media_type_s"
        "&facet.field=media_files_count_i"
        "&facet.range=duration_i&f.duration_i.facet.range.start=0&f.duration_i.facet.range.end=36000&f.duration_i.facet.range.gap=3600"
        "&facet.range=production_date_dt&f.production_date_dt.facet.range.start=1900-01-01T00:00:00Z/YEAR&f.production_date_dt.facet.range.end=NOW%2B1YEAR/YEAR&f.production_date_dt.facet.range.gap=%2B1YEAR"
        "&debug=all"
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
