from bs4 import BeautifulSoup
from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient

from app import app

app.debug = True


def test_admin_dashboard():
    with TestClient(app=app) as client:
        response = client.get('/admin')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        assert h1.get_text() == 'Admin Dashboard'
