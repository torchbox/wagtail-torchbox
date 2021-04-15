# Generated by Django 2.2.17 on 2021-04-12 10:47

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0022_auto_20210412_1042"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="valuespage", options={"verbose_name": "Values Page"},
        ),
        migrations.AddField(
            model_name="valuespage",
            name="standout_items",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "item",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("subtitle", wagtail.core.blocks.CharBlock()),
                                ("title", wagtail.core.blocks.CharBlock()),
                                ("description", wagtail.core.blocks.TextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "link",
                                    wagtail.core.blocks.StreamBlock(
                                        [
                                            (
                                                "internal",
                                                wagtail.core.blocks.PageChooserBlock(),
                                            ),
                                            (
                                                "external",
                                                wagtail.core.blocks.URLBlock(),
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
