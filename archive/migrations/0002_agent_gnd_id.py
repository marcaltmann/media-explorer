# Generated by Django 5.0.6 on 2024-06-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="agent",
            name="gnd_id",
            field=models.CharField(
                blank=True,
                help_text="<a href='https://d-nb.info/standards/elementset/gnd'>GND</a> authority file identifier",
                max_length=20,
                verbose_name="GND id",
            ),
        ),
    ]