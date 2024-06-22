# Generated by Django 5.0.6 on 2024-06-22 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0004_resource_archive_res_title_d94d90_idx"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="topicreference",
            name="resource",
        ),
        migrations.RemoveField(
            model_name="topicreference",
            name="topic",
        ),
        migrations.RemoveField(
            model_name="resource",
            name="topics",
        ),
        migrations.AlterModelOptions(
            name="collection",
            options={"ordering": ["name"]},
        ),
        migrations.AddIndex(
            model_name="collection",
            index=models.Index(fields=["name"], name="archive_col_name_311250_idx"),
        ),
        migrations.DeleteModel(
            name="TopicReference",
        ),
    ]