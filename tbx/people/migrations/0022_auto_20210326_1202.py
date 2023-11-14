# Generated by Django 2.2.17 on 2021-03-26 12:02

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0021_rename_benefits_on_culturepage_model_"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="culturepage",
            options={"verbose_name": "Careers Page"},
        ),
        migrations.AddField(
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
