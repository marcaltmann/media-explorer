import os

import sentry_sdk


ALLOWED_HOSTS = ["www.media-explorer.net", "media-explorer.net"]

INSTALLED_APPS += []


# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
SERVER_EMAIL = "info@example.com"
DEFAULT_FROM_EMAIL = "info@example.com"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


# Error Tracking

sentry_url = os.environ.get("SENTRY_URL")
if sentry_url:
    sentry_sdk.init(
        dsn=sentry_url,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
