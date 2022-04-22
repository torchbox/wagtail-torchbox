# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields
import wagtail.blocks
import tbx.core.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0003_auto_20150313_1717"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                [
                    (b"h2", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"h3", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"h4", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (b"paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
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
                            label="Aligned image",
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
                                (b"text", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    ),
                    (
                        b"pullquote",
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
                    (
                        b"raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                ],
                default="",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="standardpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                [
                    (b"h2", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"h3", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"h4", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (b"paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
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
                            label="Aligned image",
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
                                (b"text", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    ),
                    (
                        b"pullquote",
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
                    (
                        b"raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                ],
                default="",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="workpage",
            name="streamfield",
            field=wagtail.fields.StreamField(
                [
                    (b"h2", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"h3", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"h4", wagtail.blocks.CharBlock(classname="title", icon="title"),),
                    (b"intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    (b"paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
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
                            label="Aligned image",
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
                                (b"text", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    ),
                    (
                        b"pullquote",
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
                    (
                        b"raw_html",
                        wagtail.blocks.RawHTMLBlock(icon="code", label="Raw HTML"),
                    ),
                ]
            ),
            preserve_default=True,
        ),
    ]
