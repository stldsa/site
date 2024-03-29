# Generated by Django 4.1.4 on 2023-01-03 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("committees", "0053_remove_committeespage_repeat_in_subnav_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="committeepage",
            name="formation_type",
            field=models.CharField(
                choices=[
                    ("CT", "Committee"),
                    ("WG", "Working Group"),
                    ("CU", "Caucus"),
                ],
                default="",
                max_length=2,
            ),
        ),
    ]
