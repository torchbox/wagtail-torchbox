# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-20 16:31
from __future__ import unicode_literals

from django.db import migrations
import tbx.core.blocks
import wagtail.core.blocks
import wagtail.core.fields
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
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("alignment", tbx.core.blocks.ImageFormatChoiceBlock()),
                                ("caption", wagtail.core.blocks.CharBlock()),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(required=False),
                                ),
                            ),
                            label="Aligned image",
                        ),
                    ),
                    (
                        "wide_image",
                        wagtail.core.blocks.StructBlock(
                            (("image", wagtail.images.blocks.ImageChooserBlock()),),
                            label="Wide image",
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("text", wagtail.core.blocks.RichTextBlock()),
                            )
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "quote",
                                    wagtail.core.blocks.CharBlock(
                                        classname="quote title"
                                    ),
                                ),
                                ("attribution", wagtail.core.blocks.CharBlock()),
                            )
                        ),
                    ),
                    (
                        "raw_html",
                        wagtail.core.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                )
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="streamfield",
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("alignment", tbx.core.blocks.ImageFormatChoiceBlock()),
                                ("caption", wagtail.core.blocks.CharBlock()),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(required=False),
                                ),
                            ),
                            label="Aligned image",
                        ),
                    ),
                    (
                        "wide_image",
                        wagtail.core.blocks.StructBlock(
                            (("image", wagtail.images.blocks.ImageChooserBlock()),),
                            label="Wide image",
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("text", wagtail.core.blocks.RichTextBlock()),
                            )
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "quote",
                                    wagtail.core.blocks.CharBlock(
                                        classname="quote title"
                                    ),
                                ),
                                ("attribution", wagtail.core.blocks.CharBlock()),
                            )
                        ),
                    ),
                    (
                        "raw_html",
                        wagtail.core.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                )
            ),
        ),
        migrations.AlterField(
            model_name="workpage",
            name="streamfield",
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("alignment", tbx.core.blocks.ImageFormatChoiceBlock()),
                                ("caption", wagtail.core.blocks.CharBlock()),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(required=False),
                                ),
                            ),
                            label="Aligned image",
                        ),
                    ),
                    (
                        "wide_image",
                        wagtail.core.blocks.StructBlock(
                            (("image", wagtail.images.blocks.ImageChooserBlock()),),
                            label="Wide image",
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("text", wagtail.core.blocks.RichTextBlock()),
                            )
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "quote",
                                    wagtail.core.blocks.CharBlock(
                                        classname="quote title"
                                    ),
                                ),
                                ("attribution", wagtail.core.blocks.CharBlock()),
                            )
                        ),
                    ),
                    (
                        "raw_html",
                        wagtail.core.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")),
                )
            ),
        ),
    ]
