# Generated by Django 4.1.7 on 2023-04-04 03:57

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("committees", "0054_alter_committeepage_formation_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormationsPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("description", wagtail.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
