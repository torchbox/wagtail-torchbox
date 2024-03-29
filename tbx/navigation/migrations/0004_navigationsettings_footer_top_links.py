# Generated by Django 2.2.17 on 2021-07-28 13:32

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("navigation", "0003_auto_20210415_1145"),
    ]

    operations = [
        migrations.AddField(
            model_name="navigationsettings",
            name="footer_top_links",
            field=wagtail.fields.StreamField(
                [
                    (
                        "link",
                        wagtail.blocks.StructBlock(
                            [
                                ("page", wagtail.blocks.PageChooserBlock()),
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Leave blank to use the page's own title",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                help_text="Single list of links that appear between the teasers and the addresses.",
            ),
        ),
    ]
