# Generated by Django 5.0 on 2023-12-17 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("committees", "0060_alter_committeepage_leaders"),
    ]

    operations = [
        migrations.AddField(
            model_name="committeepage",
            name="gcal_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
