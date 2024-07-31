from datetime import timedelta
from django.contrib import admin
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from entities.models import Entity


class Resource(models.Model):
    TYPE_INTERVIEW = "INTERVIEW"
    TYPE_AUDIOBOOK = "AUDIOBOOK"
    TYPE_OTHER = "OTHER"
    TYPE_CHOICES = (
        (TYPE_INTERVIEW, _("Interview")),
        (TYPE_AUDIOBOOK, _("Audiobook")),
        (TYPE_OTHER, _("Other")),
    )
    type = models.CharField(
        _("type"),
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_INTERVIEW,
    )
    title = models.CharField(_("title"), max_length=200, default="")
    anon_title = models.CharField(_("anonymized title"), max_length=200, default="")
    description = models.TextField(_("description"), default="", blank=True, null=False)
    # Copyright status
    # Copyright license
    public = models.BooleanField(_("public"), default=True)
    agents = models.ManyToManyField("Agent", through="Agency", verbose_name=_("agents"))

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]
        verbose_name = _("resource")
        verbose_name_plural = _("resources")

    def duration(self):
        db_result = self.media_files.aggregate(Sum("duration"))
        return db_result["duration__sum"] or 0

    def media_type(self):
        return self.media_files.first().media_type

    def production_date(self):
        return self.media_files.first().production_date

    def char_field_metadata(self):
        return self.charfieldmetadata_set.all()

    def get_absolute_url(self):
        return reverse("archive:resource_detail", args=[self.id])

    def __str__(self):
        return self.title


class MediaFile(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name=_("resource"),
        related_name="media_files",
    )
    order = models.PositiveSmallIntegerField(_("order"), default=0)
    media_type = models.CharField(
        _("media type"),
        max_length=100,
        default="video/mp4",
        help_text="Enter MIME type e.g. 'video/mp4'.",
    )
    media_url = models.URLField(_("media url"), max_length=300, default="")
    poster = models.ImageField(_("poster image"), default="", blank=True)
    duration = models.DurationField(_("duration"), default=timedelta(seconds=0))
    production_date = models.DateTimeField(_("production date"), null=True)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["order"]),
        ]
        verbose_name = _("media file")
        verbose_name_plural = _("media files")

    def media_type_first_part(self) -> str:
        return self.media_type.split("/")[0]

    @admin.display(
        boolean=True,
        ordering="media_type",
        description="is video?",
    )
    def is_video(self) -> bool:
        return self.media_type_first_part() == "video"

    def is_audio(self) -> bool:
        return self.media_type_first_part() == "audio"

    def __str__(self):
        return f"{self.resource}-{self.order}"

    def get_absolute_url(self):
        return reverse("archive:media_file_detail", args=[self.resource_id, self.order])


class Collection(models.Model):
    resources = models.ManyToManyField(Resource, verbose_name=_("resources"))
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), default="")

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    def resource_count(self):
        return self.resources.count()

    def get_absolute_url(self):
        return reverse("archive:collection_detail", args=[self.id])

    def __str__(self):
        return self.name


class Agent(models.Model):
    MALE = "M"
    FEMALE = "F"
    DIVERSE = "D"
    UNSPECIFIED = "N"
    GENDER_CHOICES = {
        MALE: _("Male"),
        FEMALE: _("Female"),
        DIVERSE: _("Diverse"),
        UNSPECIFIED: _("Not specified"),
    }

    first_name = models.CharField(_("first name"), max_length=200, default="")
    last_name = models.CharField(_("last name"), max_length=200)
    eastern_name_order = models.BooleanField(
        _("eastern name order"),
        default=False,
        help_text=_("Select if the last name should appear first."),
    )
    gnd_id = models.CharField(
        _("GND id"),
        max_length=20,
        blank=True,
        help_text=_(
            "<a href='https://d-nb.info/standards/elementset/gnd'>GND</a> authority file identifier"
        ),
    )
    gender = models.CharField(
        _("gender"),
        max_length=1,
        choices=GENDER_CHOICES,
        default=UNSPECIFIED,
    )
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("agent")
        verbose_name_plural = _("agents")

    def fullname(self):
        if self.eastern_name_order:
            return f"{self.last_name} {self.first_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.fullname()


class Agency(models.Model):
    INTERVIEWEE = "INT"
    INTERVIEWER = "ITR"
    CAMERA = "CAM"
    SOUND = "SND"
    EDITOR = "EDT"
    OTHER = "OTH"
    TYPE_CHOICES = {
        INTERVIEWEE: _("Interviewee"),
        INTERVIEWER: _("Interviewer"),
        CAMERA: _("Camera"),
        SOUND: _("Sound"),
        EDITOR: _("Editor"),
        OTHER: _("Other"),
    }

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name=_("agent"))
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name=_("resource")
    )
    type = models.CharField(
        _("type"), max_length=3, choices=TYPE_CHOICES, default=INTERVIEWEE
    )

    class Meta:
        verbose_name = _("agency")
        verbose_name_plural = _("agencies")

    def __str__(self):
        return "{}_{}".format(self.agent.__str__(), self.resource.__str__())


class EntityReference(models.Model):
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, verbose_name=_("entity")
    )
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
        verbose_name = _("entity reference")
        verbose_name_plural = _("entity references")

    def __str__(self):
        return f"{self.entity}_{self.resource}"


class MetadataKey(models.Model):
    label = models.CharField(_("label"), max_length=20)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("metadata key")
        verbose_name_plural = _("metadata keys")

    def char_fields_for_resource(self, resource_id):
        return self.charfieldmetadata_set.all().filter(resource_id=resource_id)

    def __str__(self):
        return self.label


class CharFieldMetadata(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name=_("resource")
    )
    key = models.ForeignKey(
        MetadataKey, on_delete=models.CASCADE, verbose_name=_("key")
    )
    value = models.CharField(_("value"), max_length=200)

    class Meta:
        verbose_name = _("char field metadata")
        verbose_name_plural = _("char field metadata")

    def __str__(self):
        return self.value
