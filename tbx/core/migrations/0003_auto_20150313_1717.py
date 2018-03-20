# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks
import tbx.core.models
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0002_workpage_streamfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workpage',
            name='streamfield',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.core.blocks.CharBlock()), (b'attribution', wagtail.core.blocks.CharBlock(required=False))], label='Aligned image')), ('photogrid', wagtail.core.blocks.StructBlock([(b'images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), ('bustout', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'text', wagtail.core.blocks.RichTextBlock())])), ('pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.core.blocks.CharBlock())])), ('stats', wagtail.core.blocks.StructBlock([])), ('raw_html', wagtail.core.blocks.RawHTMLBlock(icon='code', label='Raw HTML'))]),
            preserve_default=True,
        ),
    ]
