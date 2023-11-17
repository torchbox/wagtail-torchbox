# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields
import wagtail.blocks
import tbx.core.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0002_workpage_streamfield"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                [
                    ("h2", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    ("h3", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    ("h4", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "aligned_image",
                        wagtail.blocks.StructBlock(
                            [
                                (b"image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    b"alignment",
                                    tbx.core.blocks.ImageFormatChoiceBlock(),
                                ),
                                (b"caption", wagtail.blocks.CharBlock()),
                                (
                                    b"attribution",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            label="Aligned image",
                        ),
                    ),
                    (
                        "photogrid",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b"images",
                                    wagtail.blocks.ListBlock(
                                        wagtail.images.blocks.ImageChooserBlock()
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "bustout",
                        wagtail.blocks.StructBlock(
                            [
                                (b"image", wagtail.images.blocks.ImageChooserBlock()),
                                (b"text", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    ),
                    (
                        "pullquote",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b"quote",
                                    wagtail.blocks.CharBlock(classname="quote title"),
                                ),
                                (b"attribution", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                    ("stats", wagtail.blocks.StructBlock([])),
                    (
                        "raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                ]
            ),
            preserve_default=True,
        ),
    ]
