# Generated by Django 4.2.7 on 2023-11-14 04:43

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0009_joinpage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="joinpage",
            name="description",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
