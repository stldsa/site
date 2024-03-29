# Generated by Django 4.2.7 on 2023-11-09 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0008_eventpage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventpage",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="events.event"
            ),
        ),
    ]
