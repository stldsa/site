# Generated by Django 4.1.4 on 2022-12-30 21:33

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0042_alter_newspage_main_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newspage",
            name="main_event",
            field=modelcluster.fields.ParentalKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.event",
            ),
        ),
    ]
