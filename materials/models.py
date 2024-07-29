from django.db import models
from django.utils.translation import gettext_lazy as _

from archive.models import Resource, MediaFile


class Transcript(models.Model):
    media_file = models.ForeignKey(
        MediaFile,
        on_delete=models.CASCADE,
        verbose_name=_("media file"),
    )
    json = models.JSONField(
        _("JSON file"),
        default=list,
        help_text=_("Paste the full transcript in JSON format."),
    )
    vtt = models.TextField(
        _("VTT file"),
        default="",
        help_text=_("Paste the full transcript in VTT format."),
    )
    language = models.CharField(_("language"), max_length=5)

    class Meta:
        verbose_name = _("transcript")
        verbose_name_plural = _("transcripts")

    def __str__(self):
        return f"{self.media_file} ({self.language})"


class Material(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name=_("resource")
    )
    identifier = models.CharField(_("identifier"), max_length=50)
    caption = models.CharField(_("caption"), max_length=255, blank=True)
    date = models.DateField(_("date"), null=True, blank=True)
    license = models.CharField(_("license"), max_length=255, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("material")
        verbose_name_plural = _("materials")

    def __str__(self):
        return self.identifier


class TextMaterial(Material):
    content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("text material")
        verbose_name_plural = _("text materials")


class ImageMaterial(Material):
    image = models.ImageField(_("image"))

    class Meta:
        verbose_name = _("image material")
        verbose_name_plural = _("image materials")
