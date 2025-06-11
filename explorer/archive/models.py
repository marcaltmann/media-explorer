from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Archive(models.Model):
    """Represents the most basic collection of resources."""

    name = models.CharField(_("name"), max_length=200, db_index=True)
    description = models.TextField(_("description"), blank=True, null=False)
    preview_image = models.ImageField(
        _("preview image"), default=None, null=True, blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("archive")
        verbose_name_plural = _("archives")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """This does not make sense in single archive mode."""
        return reverse("archive:archive_detail", kwargs={"pk": self.pk})
