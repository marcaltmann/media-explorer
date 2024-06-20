# Generated by Django 5.0.6 on 2024-06-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0003_alter_locationreference_location_and_more"),
        ("entities", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="resource",
            index=models.Index(fields=["title"], name="archive_res_title_d94d90_idx"),
        ),
    ]
