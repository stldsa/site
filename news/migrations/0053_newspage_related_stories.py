# Generated by Django 3.2.14 on 2022-07-06 16:40

from django.db import migrations
import news.models
import stl_dsa.utils.storage_backends
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0052_remove_newspage_related_stories'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspage',
            name='related_stories',
            field=wagtail.fields.StreamField([('related_story', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('copy', wagtail.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(storage=stl_dsa.utils.storage_backends.select_private_storage))]))], blank=True, default=news.models.upcoming_events_as_related_stories, null=True, use_json_field=True),
        ),
    ]
