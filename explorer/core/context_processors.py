from django.conf import settings

def site(request):
    my_dict = {
        'site_name': settings.EXPLORER_SITE_NAME,
    }

    return my_dict
