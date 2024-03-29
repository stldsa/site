# Generated by Django 4.1.4 on 2022-12-31 14:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
    ]

    operations = [
        migrations.CreateModel(
            name="APICalls",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("start", models.DateTimeField()),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.CharField(blank=True, max_length=30, null=True)),
                ("city", models.CharField(blank=True, max_length=30, null=True)),
                ("state", models.CharField(blank=True, max_length=2, null=True)),
                ("zip", models.IntegerField(blank=True, null=True)),
                ("url", models.URLField()),
                ("status", models.CharField(blank=True, max_length=50, null=True)),
                ("uuid", models.UUIDField(null=True)),
            ],
            options={
                "ordering": ["-start"],
            },
        ),
        migrations.CreateModel(
            name="EventsPage",
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
                (
                    "link_url",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="link to a custom URL",
                    ),
                ),
                (
                    "url_append",
                    models.CharField(
                        blank=True,
                        help_text="Use this to optionally append a #hash or querystring to the URL.",
                        max_length=255,
                        verbose_name="append to URL",
                    ),
                ),
                (
                    "extra_classes",
                    models.CharField(
                        blank=True,
                        help_text="Optionally specify css classes to be added to this page when it appears in menus.",
                        max_length=100,
                        verbose_name="menu item css classes",
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.page",
                        verbose_name="link to an internal page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
