# Generated by Django 3.1.8 on 2021-04-13 00:35

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0011_auto_20210412_1827"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "header",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "header",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("h1", "H1"),
                                            ("h2", "H2"),
                                            ("h3", "H3"),
                                            ("h4", "H4"),
                                            ("h5", "H5"),
                                            ("h6", "H6"),
                                        ],
                                        label="Header Size",
                                    ),
                                ),
                                (
                                    "text",
                                    wagtail.core.blocks.CharBlock(
                                        label="Text", max_length=50
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("text", wagtail.core.blocks.RichTextBlock()),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    (
                        "subsection",
                        wagtail.core.blocks.StreamBlock(
                            [
                                (
                                    "header",
                                    wagtail.core.blocks.StructBlock(
                                        [
                                            (
                                                "header",
                                                wagtail.core.blocks.ChoiceBlock(
                                                    choices=[
                                                        ("h1", "H1"),
                                                        ("h2", "H2"),
                                                        ("h3", "H3"),
                                                        ("h4", "H4"),
                                                        ("h5", "H5"),
                                                        ("h6", "H6"),
                                                    ],
                                                    label="Header Size",
                                                ),
                                            ),
                                            (
                                                "text",
                                                wagtail.core.blocks.CharBlock(
                                                    label="Text", max_length=50
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                                ("text", wagtail.core.blocks.TextBlock()),
                            ]
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
    ]
