# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-20 16:31
from __future__ import unicode_literals

from django.db import migrations
import tbx.core.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtailmarkdown.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0098_auto_20180320_1138"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("alignment", tbx.core.blocks.ImageFormatChoiceBlock()),
                                ("caption", wagtail.blocks.CharBlock()),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ),
                            label="Aligned image",
                        ),
                    ),
                    (
                        "wide_image",
                        wagtail.blocks.StructBlock(
                            (("image", wagtail.images.blocks.ImageChooserBlock()),),
                            label="Wide image",
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("text", wagtail.blocks.RichTextBlock()),
                            )
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "quote",
                                    wagtail.blocks.CharBlock(classname="quote title"),
                                ),
                                ("attribution", wagtail.blocks.CharBlock()),
                            )
                        ),
                    ),
                    (
                        "raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                )
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("alignment", tbx.core.blocks.ImageFormatChoiceBlock()),
                                ("caption", wagtail.blocks.CharBlock()),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ),
                            label="Aligned image",
                        ),
                    ),
                    (
                        "wide_image",
                        wagtail.blocks.StructBlock(
                            (("image", wagtail.images.blocks.ImageChooserBlock()),),
                            label="Wide image",
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("text", wagtail.blocks.RichTextBlock()),
                            )
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "quote",
                                    wagtail.blocks.CharBlock(classname="quote title"),
                                ),
                                ("attribution", wagtail.blocks.CharBlock()),
                            )
                        ),
                    ),
                    (
                        "raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                )
            ),
        ),
        migrations.AlterField(
            model_name="workpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("alignment", tbx.core.blocks.ImageFormatChoiceBlock()),
                                ("caption", wagtail.blocks.CharBlock()),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ),
                            label="Aligned image",
                        ),
                    ),
                    (
                        "wide_image",
                        wagtail.blocks.StructBlock(
                            (("image", wagtail.images.blocks.ImageChooserBlock()),),
                            label="Wide image",
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("text", wagtail.blocks.RichTextBlock()),
                            )
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "quote",
                                    wagtail.blocks.CharBlock(classname="quote title"),
                                ),
                                ("attribution", wagtail.blocks.CharBlock()),
                            )
                        ),
                    ),
                    (
                        "raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                )
            ),
        ),
    ]
