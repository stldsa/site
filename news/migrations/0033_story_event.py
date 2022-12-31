# Generated by Django 4.1.4 on 2022-12-30 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0032_remove_story_copy_story_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="story",
            name="event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.event",
            ),
        ),
    ]
