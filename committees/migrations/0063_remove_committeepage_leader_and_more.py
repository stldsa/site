# Generated by Django 5.0 on 2023-12-17 17:11

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("committees", "0062_remove_committeepage_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="committeepage",
            name="leader",
        ),
        migrations.RemoveField(
            model_name="committeepage",
            name="leaders",
        ),
        migrations.RemoveField(
            model_name="committeepage",
            name="people",
        ),
        migrations.AlterField(
            model_name="committeepage",
            name="description",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
