# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields
import wagtail.blocks
import tbx.core.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="workpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                [
                    (
                        b"h2",
                        wagtail.blocks.CharBlock(
                            classname=b"title",
                            template=b"blocks/h2.html",
                            icon=b"title",
                        ),
                    ),
                    (
                        b"h3",
                        wagtail.blocks.CharBlock(classname=b"title", icon=b"title"),
                    ),
                    (
                        b"h4",
                        wagtail.blocks.CharBlock(classname=b"title", icon=b"title"),
                    ),
                    (b"intro", wagtail.blocks.RichTextBlock(icon=b"pilcrow")),
                    (b"paragraph", wagtail.blocks.RichTextBlock(icon=b"pilcrow")),
                    (
                        b"aligned_image",
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
                            label=b"Aligned image",
                        ),
                    ),
                    (
                        b"photogrid",
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
                        b"bustout",
                        wagtail.blocks.StructBlock(
                            [
                                (b"image", wagtail.images.blocks.ImageChooserBlock()),
                                (b"text", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                    (
                        b"pullquote",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b"quote",
                                    wagtail.blocks.CharBlock(classname=b"quote title"),
                                ),
                                (b"attribution", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                    (
                        b"testimonial",
                        wagtail.blocks.StructBlock(
                            [
                                (b"quote", wagtail.blocks.CharBlock()),
                                (b"attribution", wagtail.blocks.CharBlock()),
                                (
                                    b"image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                            ],
                            icon=b"group",
                            label=b"Testimonial",
                        ),
                    ),
                    (b"stats", wagtail.blocks.StructBlock([])),
                    (
                        b"raw_html",
                        wagtail.blocks.RawHTMLBlock(icon=b"code", label=b"Raw HTML"),
                    ),
                ]
            ),
            preserve_default=True,
        ),
    ]
