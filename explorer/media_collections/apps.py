from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MediaCollectionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "explorer.media_collections"
    verbose_name = _("Media collections")
