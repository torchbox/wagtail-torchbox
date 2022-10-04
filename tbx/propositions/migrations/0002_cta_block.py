# Generated by Django 3.2.13 on 2022-10-04 13:15

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('propositions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propositionpage',
            name='clients_section_body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading2_block.html')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading3_block.html')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading4_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='patterns/molecules/streamfield/blocks/paragraph_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionpage',
            name='services_section_body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading2_block.html')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading3_block.html')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading4_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='patterns/molecules/streamfield/blocks/paragraph_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionpage',
            name='team_section_body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading2_block.html')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading3_block.html')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading4_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='patterns/molecules/streamfield/blocks/paragraph_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionsubpage',
            name='clients_section_body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading2_block.html')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading3_block.html')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading4_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='patterns/molecules/streamfield/blocks/paragraph_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionsubpage',
            name='services_section_body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading2_block.html')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading3_block.html')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading4_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='patterns/molecules/streamfield/blocks/paragraph_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionsubpage',
            name='team_section_body',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading2_block.html')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading3_block.html')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title', template='patterns/molecules/streamfield/blocks/heading4_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='patterns/molecules/streamfield/blocks/paragraph_block.html')), ('cta', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(help_text='Words in  &lt;span&gt; tag will display in a contrasting colour.')), ('link', wagtail.blocks.StreamBlock([('internal_link', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock()), ('link_text', wagtail.blocks.CharBlock(required=False))])), ('external_link', wagtail.blocks.StructBlock([('link_url', wagtail.blocks.URLBlock(label='URL')), ('link_text', wagtail.blocks.CharBlock())]))]))], icon='plus-inverse', template='patterns/molecules/streamfield/blocks/cta.html'))], blank=True, use_json_field=True),
        ),
    ]
