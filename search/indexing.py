import requests

SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def index_resource(resource):
    url = SOLR_URL + "update/json/docs?commit=true"

    doc = {
        "id": str(resource.id),
        "title_t": resource.title,
        "description_t": resource.description,
        "transcript_t": resource.agg_transcript_texts(),
        "media_type_s": resource.media_type(),
        "duration_i": resource.duration().seconds,
        "production_date_dt": str(resource.production_date()),
        "public_b": resource.public,
    }
    requests.post(url, json=doc)


def delete_all():
    url = SOLR_URL + "update?commit=true"
    data = {
        "delete": {"query": "*:*"},
    }
    requests.post(url, json=data)


def commit():
    url = SOLR_URL + "update?commit=true"
    requests.post(url, headers={"Content-Type": "application/json"})
