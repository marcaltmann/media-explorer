# Generated by Django 5.1b1 on 2024-07-31 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "archive",
            "0003_remove_resource_duration_remove_resource_media_type_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="description",
            field=models.TextField(blank=True, default="", verbose_name="description"),
        ),
    ]
