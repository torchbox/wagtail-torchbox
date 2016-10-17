# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import tbx.core.models
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0002_workpage_streamfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workpage',
            name='streamfield',
            field=wagtail.wagtailcore.fields.StreamField([('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock()), (b'attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))], label='Aligned image')), ('photogrid', wagtail.wagtailcore.blocks.StructBlock([(b'images', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailimages.blocks.ImageChooserBlock()))])), ('bustout', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'text', wagtail.wagtailcore.blocks.RichTextBlock())])), ('pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.wagtailcore.blocks.CharBlock())])), ('stats', wagtail.wagtailcore.blocks.StructBlock([])), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code', label='Raw HTML'))]),
            preserve_default=True,
        ),
    ]
