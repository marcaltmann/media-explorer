from pytest_django.asserts import assertContains

from .views import welcome, legal_notice, accessibility, privacy, contact, terms


def test_welcome(rf):
    request = rf.get("/de/")
    response = welcome(request)
    assert response.status_code == 200


def test_legal_notice(rf):
    request = rf.get("/de/pages/legal_notice/")
    response = legal_notice(request)
    assert response.status_code == 200


def test_accessibility(rf):
    request = rf.get("/de/pages/accessibility/")
    response = accessibility(request)
    assert response.status_code == 200


def test_privacy(rf):
    request = rf.get("/de/pages/privacy/")
    response = privacy(request)
    assert response.status_code == 200


def test_contact(rf):
    request = rf.get("/de/pages/contact/")
    response = contact(request)
    assert response.status_code == 200


def test_terms(rf):
    request = rf.get("/de/pages/terms/")
    response = terms(request)
    assert response.status_code == 200


def test_footer(rf):
    request = rf.get("/de/")
    response = welcome(request)
    assertContains(response, "https://github.com/marcaltmann/explorer")
