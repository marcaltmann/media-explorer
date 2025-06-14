import environ
from pathlib import Path
import re

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


# Prepare environment

BASE_DIR = Path(__file__).resolve().parent.parent

# Some environment variables need to be set to dummy values
# or made optional so that the Docker image can be built.
# TODO: Check for presence of env variables at runtime through
# the Docker entrypoint script.
env = environ.Env(
    ALLOWED_HOSTS=(str, ""),
    DATABASE_URL=(str, "postgres://"),
    DEBUG=(bool, False),
    SECRET_KEY=(str, "dummy-secret-key-set-later"),
    SENTRY_DSN=(str, None),
    EMAIL_HOST=(str, "localhost"),
    EMAIL_PORT=(str, 25),
    EMAIL_HOST_USER=(str, None),
    EMAIL_HOST_PASSWORD=(str, None),
    EXPLORER_SITE_NAME=(str, "Elefant Explorer"),
    EXPLORER_SINGLE_COLLECTION_MODE=(bool, False),
)

environ.Env.read_env(BASE_DIR / ".env")

DJANGO_ENV = env("DJANGO_ENV")
if DJANGO_ENV not in ["development", "production", "test"]:
    raise ImproperlyConfigured(
        "DJANGO_ENV must be one of development, production or test"
    )

if DJANGO_ENV == "production":
    import sentry_sdk


# Start with settings

DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.parse_value(env("ALLOWED_HOSTS"), list)

CSRF_TRUSTED_ORIGINS = [
    "https://www.media-explorer.net",
]

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
    "explorer.media_collections",
    "explorer.my_account",
    "explorer.resources",
]
if DJANGO_ENV == "development":
    INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

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
if DJANGO_ENV == "development":
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
elif DJANGO_ENV == "production":
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")


ROOT_URLCONF = "explorer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "explorer" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "explorer.core.context_processors.site",
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
LOGIN_REDIRECT_URL = "explorer.my_account:profile"
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


# Email
DEFAULT_FROM_EMAIL = "no-reply@media-explorer.net"
SERVER_EMAIL = "admin@media-explorer.net"

if DJANGO_ENV == "development":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = "tmp/emails"
elif DJANGO_ENV == "production":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")


# Media files
# TODO: Should not be saved in the filesystem.

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "vite_assets_dist"]


if DJANGO_ENV == "production":
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "region_name": env("S3_REGION_NAME"),
                "endpoint_url": env("S3_ENDPOINT_URL"),
                "access_key": env("S3_ACCESS_KEY"),
                "secret_key": env("S3_SECRET_KEY"),
                "bucket_name": env("S3_BUCKET_NAME"),
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

if DJANGO_ENV == "development":
    DJANGO_VITE = {"default": {"dev_mode": True}}


def immutable_file_test(path, url):
    # Match vite (rollup)-generated hashes, à la, `some_file-CSliV9zW.js`
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test


# Sentry error tracking

sentry_dsn = env("SENTRY_DSN")
if DJANGO_ENV == "production" and sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


# Explorer-specific settings
# not used yet

EXPLORER_SITE_NAME = env("EXPLORER_SITE_NAME")
EXPLORER_SITE_VERSION = "v0.2"
EXPLORER_SINGLE_COLLECTION_MODE = env("EXPLORER_SINGLE_COLLECTION_MODE")
EXPLORER_SEARCH_ENGINE = "solr"
