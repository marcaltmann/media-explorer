import environ
from pathlib import Path
import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


# Prepare environment

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    ALLOWED_HOSTS=(str, "")
    DEBUG=(bool, False),
    SENTRY_URL=(str, None),
)

environ.Env.read_env(BASE_DIR / ".env")

django_env = env("DJANGO_ENV")
if django_env not in ["development", "production", "test"]:
    raise ImproperlyConfigured(
        "DJANGO_ENV must be one of development, production or test"
    )


# Start with settings

ALLOWED_HOSTS = env.parse_value(env("ALLOWED_HOSTS"), list)


INSTALLED_APPS = [
    "allauth.account",
    "allauth",
    "django_vite",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "explorer.core",
    "explorer.my_account",
]
if django_env == "development":
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions"
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if django_env == "development":
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


ROOT_URLCONF = "explorer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "explorer" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "explorer.wsgi.application"


DATABASES = {
    "default": env.db(),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "my_account.User"
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
LOGIN_REDIRECT_URL = "my_account:profile"
LOGOUT_REDIRECT_URL = "core:welcome"


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
LOCALE_PATHS = (BASE_DIR / "locale",)
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "vite_assets_dist"]


email_url = env.email_url()
EMAIL_BACKEND = email_url["EMAIL_BACKEND"]
EMAIL_FILE_PATH = email_url["EMAIL_FILE_PATH"]
EMAIL_HOST = email_url["EMAIL_HOST"]
EMAIL_PORT = email_url["EMAIL_PORT"]
EMAIL_HOST_USER = email_url["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_url["EMAIL_HOST_PASSWORD"]


# Django Vite asset management

if django_env == "development":
    DJANGO_VITE = {"default": {"dev_mode": True}}


# Explorer-specific settings
# not used yet

EXPLORER_SINGLE_ARCHIVE_MODE = False
EXPLORER_SEARCH_ENGINE = "solr"
