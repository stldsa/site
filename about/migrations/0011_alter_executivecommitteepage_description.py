# Generated by Django 4.2.7 on 2023-11-14 04:35

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("about", "0010_alter_executivecommitteepage_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="executivecommitteepage",
            name="description",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
