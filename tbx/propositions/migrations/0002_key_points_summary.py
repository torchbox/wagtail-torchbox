# Generated by Django 3.2.13 on 2022-10-12 08:28

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
            field=wagtail.fields.StreamField([('key_points_summary', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('intro', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())]), help_text='Please add a minumum of 4 and a maximum of 6 key points.', icon='list-ul', max_num=6, min_num=4, template='patterns/molecules/streamfield/blocks/key_points_summary.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionpage',
            name='services_section_body',
            field=wagtail.fields.StreamField([('key_points_summary', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('intro', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())]), help_text='Please add a minumum of 4 and a maximum of 6 key points.', icon='list-ul', max_num=6, min_num=4, template='patterns/molecules/streamfield/blocks/key_points_summary.html'))], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='propositionpage',
            name='team_section_body',
            field=wagtail.fields.StreamField([('key_points_summary', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('intro', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())]), help_text='Please add a minumum of 4 and a maximum of 6 key points.', icon='list-ul', max_num=6, min_num=4, template='patterns/molecules/streamfield/blocks/key_points_summary.html'))], blank=True, use_json_field=True),
        ),
    ]
