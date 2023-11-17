# Generated by Django 3.2.20 on 2023-11-10 09:58

from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_add_social_fields_to_all_page_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventindexpage',
            name='call_to_action',
            field=wagtail.fields.StreamField([('key_points_summary', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('intro', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())]), help_text='Please add a minumum of 3 and a maximum of 6 key points.', icon='list-ul', max_num=6, min_num=3, template='patterns/molecules/streamfield/blocks/key_points_summary.html')), ('testimonials', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('quote', wagtail.blocks.CharBlock(form_classname='quote title')), ('name', wagtail.blocks.CharBlock()), ('role', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))], required=False))]), icon='openquote', template='patterns/molecules/streamfield/blocks/testimonial_block.html')), ('clients', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))], required=False))]), icon='site', label='Clients logo', template='patterns/molecules/streamfield/blocks/client-logo-block.html')), ('embed_plus_cta', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('intro', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.blocks.URLBlock(label='External Link', required=False)), ('button_text', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('embed', wagtail.embeds.blocks.EmbedBlock(label='Youtube Embed', required=False))], icon='code', label='Embed + CTA', template='patterns/molecules/streamfield/blocks/embed_plus_cta_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
    ]
