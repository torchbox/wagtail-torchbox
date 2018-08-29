# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks
import tbx.core.models
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workpage',
            name='streamfield',
            field=wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname=b'title', template=b'blocks/h2.html', icon=b'title')), (b'h3', wagtail.core.blocks.CharBlock(classname=b'title', icon=b'title')), (b'h4', wagtail.core.blocks.CharBlock(classname=b'title', icon=b'title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon=b'pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon=b'pilcrow')), (b'aligned_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'alignment', tbx.core.models.ImageFormatChoiceBlock()), (b'caption', wagtail.core.blocks.CharBlock()), (b'attribution', wagtail.core.blocks.CharBlock(required=False))], label=b'Aligned image')), (b'photogrid', wagtail.core.blocks.StructBlock([(b'images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])), (b'bustout', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'text', wagtail.core.blocks.CharBlock())])), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.CharBlock(classname=b'quote title')), (b'attribution', wagtail.core.blocks.CharBlock())])), (b'testimonial', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.CharBlock()), (b'attribution', wagtail.core.blocks.CharBlock()), (b'image', wagtail.images.blocks.ImageChooserBlock(required=False))], icon=b'group', label=b'Testimonial')), (b'stats', wagtail.core.blocks.StructBlock([])), (b'raw_html', wagtail.core.blocks.RawHTMLBlock(icon=b'code', label=b'Raw HTML'))]),
            preserve_default=True,
        ),
    ]
