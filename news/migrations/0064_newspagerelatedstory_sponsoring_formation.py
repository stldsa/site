# Generated by Django 4.1.7 on 2023-02-25 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("committees", "0054_alter_committeepage_formation_type"),
        ("news", "0063_newspagerelatedstory_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="newspagerelatedstory",
            name="sponsoring_formation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sponsoring_formation",
                to="committees.committeepage",
            ),
        ),
    ]
