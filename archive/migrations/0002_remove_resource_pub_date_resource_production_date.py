# Generated by Django 5.1b1 on 2024-07-26 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resource",
            name="pub_date",
        ),
        migrations.AddField(
            model_name="resource",
            name="production_date",
            field=models.DateTimeField(null=True, verbose_name="production date"),
        ),
    ]
