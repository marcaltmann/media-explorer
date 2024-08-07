# Generated by Django 5.1b1 on 2024-08-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0004_resource_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mediafile",
            name="media_type",
        ),
        migrations.AddField(
            model_name="mediafile",
            name="subtype",
            field=models.CharField(
                default="mp4",
                help_text="Enter second part of MIME type e.g. 'mp4'.",
                max_length=100,
                verbose_name="subtype",
            ),
        ),
        migrations.AddField(
            model_name="mediafile",
            name="type",
            field=models.CharField(
                default="video",
                help_text="Enter first part of MIME type e.g. 'video'.",
                max_length=100,
                verbose_name="media type",
            ),
        ),
    ]
