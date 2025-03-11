from .settings_base import *

SECRET_KEY = "django-insecure-e#072wzvkw6s0m-z@e(tr1oqqu3vb7yv7-x4fxj^kh32%ag+n4"

DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += []


# Database

DATABASES = {
    "test": {
        "OPTIONS": {
            "read_default_file": str("my.cnf.test"),
        },
    },
}


# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
