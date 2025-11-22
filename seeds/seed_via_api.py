import requests

HOST = "http://127.0.0.1:8000"

TOC_ENDPOINT = "/resources/1/toc"

r = requests.get(HOST + TOC_ENDPOINT)
toc = r.json()

for idx, chapter in enumerate(toc):
    print(f"{idx + 1}: {chapter['name']} ({chapter['position']})")
