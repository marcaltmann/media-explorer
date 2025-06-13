from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from explorer.media_collections.models import Collection


class Resource(models.Model):
    """
    Represents a media resource, e.g. video, audio or photo.
    Rather abstract, independent of real files.
    """

    name = models.CharField(_("name"), max_length=255)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="resources",
        related_query_name="resource",
        verbose_name=_("collection"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("resource")
        verbose_name_plural = _("resources")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("resources:resource-detail", kwargs={"pk": self.pk})


class MediaFile(models.Model):
    """
    Represents a file of a media resource, e.g. a video or audio file or
    an image. A resource can have zero to n media files. A media file can
    be a part of a resource (e.g. a video can consist of many video files)
    or represent different versions of them (e.g. a photo with and without
    edits).
    """

    name = models.CharField(_("name"), max_length=255, blank=True, default="")
    order = models.IntegerField(_("order"))
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="media_files",
        related_query_name="media_file",
        verbose_name=_("resource"),
    )
    file = models.FileField(_("file"))

    class Meta:
        ordering = ["order"]
        verbose_name = _("media file")
        verbose_name_plural = _("media files")

    def __str__(self):
        return f"{self.order}-{self.name}"

    def get_absolute_url(self):
        return reverse("resources:media-file-detail", kwargs={"pk": self.pk})
