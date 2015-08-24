# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks
import tbx.core.models
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0012_auto_20150703_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='streamfield',
            field=wagtail.wagtailcore.fields.StreamField([(b'h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock()), (b'attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))], label='Aligned image')), (b'bustout', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'text', wagtail.wagtailcore.blocks.RichTextBlock())])), (b'pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.wagtailcore.blocks.CharBlock())])), (b'raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code', label='Raw HTML')), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='code'))]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='streamfield',
            field=wagtail.wagtailcore.fields.StreamField([(b'h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock()), (b'attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))], label='Aligned image')), (b'bustout', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'text', wagtail.wagtailcore.blocks.RichTextBlock())])), (b'pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.wagtailcore.blocks.CharBlock())])), (b'raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code', label='Raw HTML')), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='code'))]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workpage',
            name='streamfield',
            field=wagtail.wagtailcore.fields.StreamField([(b'h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock()), (b'attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))], label='Aligned image')), (b'bustout', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'text', wagtail.wagtailcore.blocks.RichTextBlock())])), (b'pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.wagtailcore.blocks.CharBlock())])), (b'raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code', label='Raw HTML')), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='code'))]),
            preserve_default=True,
        ),
    ]
