from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from archive.models import Resource


class User(AbstractUser):
    pass


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name=_("resource")
    )
    timecodes = models.JSONField(
        _("timecodes"),
        default=list,
        help_text=_(
            "Enter timecodes in seconds as a comma separated list, e.g.: [124.3, 210.5]"
        ),
    )

    class Meta:
        verbose_name = _("bookmark")
        verbose_name_plural = _("bookmarks")

    def __str__(self):
        return f"{self.user}_{self.resource}"
