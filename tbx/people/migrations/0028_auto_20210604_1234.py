# Generated by Django 2.2.17 on 2021-06-04 11:34

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0027_merge_20210603_1719"),
    ]

    operations = [
        migrations.AlterField(
            model_name="culturepage",
            name="standout_items",
            field=wagtail.fields.StreamField(
                [
                    (
                        "item",
                        wagtail.blocks.StructBlock(
                            [
                                ("subtitle", wagtail.blocks.CharBlock()),
                                ("title", wagtail.blocks.CharBlock()),
                                ("description", wagtail.blocks.TextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "link",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "internal",
                                                wagtail.blocks.PageChooserBlock(),
                                            ),
                                            (
                                                "external",
                                                wagtail.blocks.URLBlock(),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
    ]
