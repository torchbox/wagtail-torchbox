# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import tbx.core.models
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workpage',
            name='streamfield',
            field=wagtail.wagtailcore.fields.StreamField([(b'h2', wagtail.wagtailcore.blocks.CharBlock(classname=b'title', template=b'blocks/h2.html', icon=b'title')), (b'h3', wagtail.wagtailcore.blocks.CharBlock(classname=b'title', icon=b'title')), (b'h4', wagtail.wagtailcore.blocks.CharBlock(classname=b'title', icon=b'title')), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'pilcrow')), (b'aligned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock()), (b'attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))], label=b'Aligned image')), (b'photogrid', wagtail.wagtailcore.blocks.StructBlock([(b'images', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailimages.blocks.ImageChooserBlock()))])), (b'bustout', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'text', wagtail.wagtailcore.blocks.CharBlock())])), (b'pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(classname=b'quote title')), (b'attribution', wagtail.wagtailcore.blocks.CharBlock())])), (b'testimonial', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock()), (b'attribution', wagtail.wagtailcore.blocks.CharBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))], icon=b'group', label=b'Testimonial')), (b'stats', wagtail.wagtailcore.blocks.StructBlock([])), (b'raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon=b'code', label=b'Raw HTML'))]),
            preserve_default=True,
        ),
    ]
