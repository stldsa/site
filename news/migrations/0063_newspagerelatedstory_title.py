# Generated by Django 4.1.7 on 2023-02-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0062_rename_image_newspagerelatedstory_related_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="newspagerelatedstory",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
