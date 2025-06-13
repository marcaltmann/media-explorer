from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Resource(models.Model):
    """Represents a media resource, e.g. video, audio or photo."""
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = _("resource")
        verbose_name_plural = _("resources")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("resources:resource-detail", kwargs={"pk": self.pk})
