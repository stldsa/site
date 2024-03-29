# Generated by Django 4.1.4 on 2022-12-31 06:04

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0051_newspagerelatedstory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newspagerelatedstory",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="more_stories",
                to="news.newspage",
            ),
        ),
    ]
