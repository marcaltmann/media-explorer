from bs4 import BeautifulSoup
from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient

from app import app

app.debug = True


def test_contact_page():
    with TestClient(app=app) as client:
        response = client.get('/pages/contact')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        assert h1.get_text() == 'Contact'


def test_privacy_page():
    with TestClient(app=app) as client:
        response = client.get('/pages/privacy')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        assert h1.get_text() == 'Privacy'


def test_accessibility_page():
    with TestClient(app=app) as client:
        response = client.get('/pages/accessibility')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        assert h1.get_text() == 'Accessibility'


def test_terms_page():
    with TestClient(app=app) as client:
        response = client.get('/pages/terms-of-use')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        assert h1.get_text() == 'Terms of Use'


def test_legal_notice_page():
    with TestClient(app=app) as client:
        response = client.get('/pages/legal-notice')
        assert response.status_code == HTTP_200_OK

        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        assert h1.get_text() == 'Legal Notice'
