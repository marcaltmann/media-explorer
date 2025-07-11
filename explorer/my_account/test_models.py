import pytest

from django.contrib.auth import get_user_model
from django.test.utils import override_settings


User = get_user_model()


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    with override_settings(**TEST_SETTINGS):
        yield


TEST_SETTINGS = {
    "PASSWORD_HASHERS": [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ],
}


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
    assert User.objects.count() == 1
    assert user.username == "john"
    assert user.email == "lennon@thebeatles.com"
