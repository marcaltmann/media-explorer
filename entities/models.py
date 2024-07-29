from django.db import models
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django.urls import reverse


class Entity(models.Model):
    TYPE_PERSON = "PER"
    TYPE_LOCATION = "LOC"
    TYPE_ORGANISATION = "ORG"
    TYPE_MISC = "MISC"
    TYPE_CHOICES = (
        (TYPE_PERSON, _("Person")),
        (TYPE_LOCATION, _("Location")),
        (TYPE_ORGANISATION, _("Organisation")),
        (TYPE_MISC, _("Misc")),
    )
    type = models.CharField(
        _("type"),
        max_length=20,
        choices=TYPE_CHOICES,
    )
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    gnd_id = models.CharField(
        _("GND id"),
        max_length=20,
        blank=True,
        help_text=_(
            "<a href='https://d-nb.info/standards/elementset/gnd'>GND</a> authority file identifier"
        ),
    )
    extra = models.JSONField(
        _("extra"),
        default=dict,
        blank=True,
        help_text=_("Extra information specific to entity types"),
    )

    class Meta:
        indexes = (models.Index(fields=["type"]),)
        ordering = ["name"]
        verbose_name = _("entity")
        verbose_name_plural = _("entities")

    def get_absolute_url(self):
        return reverse("entities:entity_detail", args=[self.id])

    def __str__(self):
        return self.name


# class Person(models.Model):
#     MALE = "M"
#     FEMALE = "F"
#     GENDER_CHOICES = {
#         MALE: _("Male"),
#         FEMALE: _("Female"),
#     }
#     sex = models.CharField(
#         pgettext_lazy("like gender", "sex"),
#         max_length=1,
#         choices=GENDER_CHOICES,
#         blank=True,
#     )
#     date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
#     date_of_death = models.DateField(_("date of death"), blank=True, null=True)
#
#     class Meta:
#         verbose_name = _("person")
#         verbose_name_plural = _("people")
#
#
# class Location(models.Model):
#     geonames_id = models.IntegerField(
#         _("GeoNames id"),
#         blank=True,
#         null=True,
#         help_text=_(
#             "<a href='https://www.geonames.org/'>GeoNames</a> geographical database identifier"
#         ),
#     )
#     latitude = models.FloatField(_("latitude"), blank=True, null=True)
#     longitude = models.FloatField(_("longitude"), blank=True, null=True)
#
#     class Meta:
#         verbose_name = _("location")
#         verbose_name_plural = _("locations")
