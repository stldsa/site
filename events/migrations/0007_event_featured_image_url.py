# Generated by Django 4.2.6 on 2023-10-31 09:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0006_delete_eventspage"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="featured_image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
