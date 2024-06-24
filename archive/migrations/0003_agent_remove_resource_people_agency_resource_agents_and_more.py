# Generated by Django 5.0.6 on 2024-06-24 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0002_remove_resource_locations_and_more"),
        ("entities", "0003_alter_person_options_remove_person_date_of_birth_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "entity_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="entities.entity",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        default="", max_length=200, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(max_length=200, verbose_name="last name"),
                ),
                (
                    "eastern_name_order",
                    models.BooleanField(
                        default=False,
                        help_text="Select if the last name should appear first.",
                        verbose_name="eastern name order",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("M", "Male"),
                            ("F", "Female"),
                            ("D", "Diverse"),
                            ("N", "Not specified"),
                        ],
                        default="N",
                        max_length=1,
                        verbose_name="gender",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="date of birth"
                    ),
                ),
            ],
            options={
                "verbose_name": "agent",
                "verbose_name_plural": "agents",
                "ordering": ["last_name", "first_name"],
            },
            bases=("entities.entity",),
        ),
        migrations.RemoveField(
            model_name="resource",
            name="people",
        ),
        migrations.CreateModel(
            name="Agency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("INT", "Interviewee"),
                            ("ITR", "Interviewer"),
                            ("CAM", "Camera"),
                            ("SND", "Sound"),
                            ("EDT", "Editor"),
                            ("OTH", "Other"),
                        ],
                        default="INT",
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive.resource",
                        verbose_name="resource",
                    ),
                ),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive.agent",
                        verbose_name="agent",
                    ),
                ),
            ],
            options={
                "verbose_name": "agency",
                "verbose_name_plural": "agencies",
            },
        ),
        migrations.AddField(
            model_name="resource",
            name="agents",
            field=models.ManyToManyField(
                through="archive.Agency", to="archive.agent", verbose_name="agents"
            ),
        ),
        migrations.DeleteModel(
            name="ResourceInvolvement",
        ),
    ]
