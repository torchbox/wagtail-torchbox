# Generated by Django 2.2.17 on 2021-04-14 13:57

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("navigation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="navigationsettings",
            name="footer_teasers",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "link",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("page", wagtail.core.blocks.PageChooserBlock()),
                                (
                                    "title",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="Leave blank to use the page's own title",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                help_text="Row of links that use prominent styles to standout.",
            ),
        ),
    ]