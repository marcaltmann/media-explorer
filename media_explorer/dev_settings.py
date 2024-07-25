from django.utils.translation import gettext_lazy as _

from media_explorer.settings import *


LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]
LOCALE_PATHS = (BASE_DIR / "locale",)
