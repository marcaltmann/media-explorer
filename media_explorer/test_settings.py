from media_explorer.settings import *


INSTALLED_APPS = [
    "archive.apps.ArchiveConfig",
    "entities.apps.EntitiesConfig",
    "materials.apps.MaterialsConfig",
    "pages.apps.PagesConfig",
    "accounts.apps.AccountsConfig",
    "search.apps.SearchConfig",
    "api.apps.ApiConfig",
    "rest_framework",
    "widget_tweaks",
    "django_vite_plugin",
    "django_htmx",
    "django_json_widget",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]
