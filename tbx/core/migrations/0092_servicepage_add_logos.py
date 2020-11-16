# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-07 12:47


from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0091_auto_20170201_1043"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicepage",
            name="streamfield",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        b"case_studies",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    b"title",
                                    wagtail.core.blocks.CharBlock(required=True),
                                ),
                                (
                                    b"intro",
                                    wagtail.core.blocks.TextBlock(required=True),
                                ),
                                (
                                    b"case_studies",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "page",
                                                    wagtail.core.blocks.PageChooserBlock(
                                                        "torchbox.WorkPage"
                                                    ),
                                                ),
                                                (
                                                    "title",
                                                    wagtail.core.blocks.CharBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "descriptive_title",
                                                    wagtail.core.blocks.CharBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        b"highlights",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    b"title",
                                    wagtail.core.blocks.CharBlock(required=True),
                                ),
                                (
                                    b"intro",
                                    wagtail.core.blocks.TextBlock(required=False),
                                ),
                                (
                                    b"highlights",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.TextBlock()
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        b"pull_quote",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    b"quote",
                                    wagtail.core.blocks.CharBlock(
                                        classname="quote title"
                                    ),
                                ),
                                (b"attribution", wagtail.core.blocks.CharBlock()),
                            ],
                            template="blocks/pull_quote_block.html",
                        ),
                    ),
                    (
                        b"process",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    b"title",
                                    wagtail.core.blocks.CharBlock(required=True),
                                ),
                                (
                                    b"intro",
                                    wagtail.core.blocks.TextBlock(required=False),
                                ),
                                (
                                    b"steps",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "subtitle",
                                                    wagtail.core.blocks.CharBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "title",
                                                    wagtail.core.blocks.CharBlock(
                                                        required=True
                                                    ),
                                                ),
                                                (
                                                    "icon",
                                                    wagtail.core.blocks.CharBlock(
                                                        help_text="Paste SVG code here",
                                                        max_length=9000,
                                                        required=True,
                                                    ),
                                                ),
                                                (
                                                    "description",
                                                    wagtail.core.blocks.TextBlock(
                                                        required=True
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        b"people",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    b"title",
                                    wagtail.core.blocks.CharBlock(required=True),
                                ),
                                (
                                    b"intro",
                                    wagtail.core.blocks.TextBlock(required=True),
                                ),
                                (
                                    b"people",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.PageChooserBlock()
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        b"featured_pages",
                        wagtail.core.blocks.StructBlock(
                            [
                                (b"title", wagtail.core.blocks.CharBlock()),
                                (
                                    b"pages",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "page",
                                                    wagtail.core.blocks.PageChooserBlock(),
                                                ),
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(),
                                                ),
                                                (
                                                    "text",
                                                    wagtail.core.blocks.TextBlock(),
                                                ),
                                                (
                                                    "sub_text",
                                                    wagtail.core.blocks.CharBlock(
                                                        max_length=100
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        b"sign_up_form_page",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    b"page",
                                    wagtail.core.blocks.PageChooserBlock(
                                        "torchbox.SignUpFormPage"
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        b"logos",
                        wagtail.core.blocks.StructBlock(
                            [
                                (b"title", wagtail.core.blocks.CharBlock()),
                                (b"intro", wagtail.core.blocks.CharBlock()),
                                (
                                    b"logos",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(),
                                                ),
                                                (
                                                    "link_page",
                                                    wagtail.core.blocks.PageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "link_external",
                                                    wagtail.core.blocks.URLBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                ]
            ),
        ),
    ]
