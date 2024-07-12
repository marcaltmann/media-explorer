import requests

SOLR_URL = "http://localhost:8983/solr/media_explorer/"


def index_resource(resource):
    url = SOLR_URL + "update/json/docs"
    doc = {
        "title_s": resource.title,
        "media_type_s": resource.media_type,
        "pub_date_dt": str(resource.pub_date),
        "public_b": resource.public,
    }
    response = requests.post(url, json=doc)
    print(response.json())


def commit():
    url = SOLR_URL + "update?commit=true"
    response = requests.post(url, headers={"Content-Type": "application/json"})
    print(response.json())
