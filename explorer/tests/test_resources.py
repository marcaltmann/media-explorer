from bs4 import BeautifulSoup
from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient

from app import app

app.debug = True


def test_resource_detail_page():
    with TestClient(app=app) as client:
        response = client.get('/resources/7')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('h1').find('a')
        assert link.get_text() == 'Again to the Front (1952)'
