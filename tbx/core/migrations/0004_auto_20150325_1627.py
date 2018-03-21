# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks
import tbx.core.models
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0003_auto_20150313_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='streamfield',
            field=wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.core.blocks.CharBlock()), (b'attribution', wagtail.core.blocks.CharBlock(required=False))], label='Aligned image')), (b'photogrid', wagtail.core.blocks.StructBlock([(b'images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), (b'bustout', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'text', wagtail.core.blocks.RichTextBlock())])), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.core.blocks.CharBlock())])), (b'raw_html', wagtail.core.blocks.RawHTMLBlock(icon='code', label='Raw HTML'))], default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standardpage',
            name='streamfield',
            field=wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.core.blocks.CharBlock()), (b'attribution', wagtail.core.blocks.CharBlock(required=False))], label='Aligned image')), (b'photogrid', wagtail.core.blocks.StructBlock([(b'images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), (b'bustout', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'text', wagtail.core.blocks.RichTextBlock())])), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.core.blocks.CharBlock())])), (b'raw_html', wagtail.core.blocks.RawHTMLBlock(icon='code', label='Raw HTML'))], default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workpage',
            name='streamfield',
            field=wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.core.blocks.CharBlock()), (b'attribution', wagtail.core.blocks.CharBlock(required=False))], label='Aligned image')), (b'photogrid', wagtail.core.blocks.StructBlock([(b'images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), (b'bustout', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'text', wagtail.core.blocks.RichTextBlock())])), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.CharBlock(classname='quote title')), (b'attribution', wagtail.core.blocks.CharBlock())])), (b'raw_html', wagtail.core.blocks.RawHTMLBlock(icon='code', label='Raw HTML'))]),
            preserve_default=True,
        ),
    ]
