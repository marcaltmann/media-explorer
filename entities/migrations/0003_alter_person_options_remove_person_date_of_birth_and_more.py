# Generated by Django 5.0.6 on 2024-06-24 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("entities", "0002_alter_organisation_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="person",
            options={"verbose_name": "person", "verbose_name_plural": "people"},
        ),
        migrations.RemoveField(
            model_name="person",
            name="date_of_birth",
        ),
        migrations.RemoveField(
            model_name="person",
            name="eastern_name_order",
        ),
        migrations.RemoveField(
            model_name="person",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="person",
            name="gender",
        ),
        migrations.RemoveField(
            model_name="person",
            name="last_name",
        ),
    ]
