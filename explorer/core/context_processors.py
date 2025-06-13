from django.conf import settings


def site(request):
    my_dict = {
        "site_name": settings.EXPLORER_SITE_NAME,
        "site_version": settings.EXPLORER_SITE_VERSION,
    }

    return my_dict
