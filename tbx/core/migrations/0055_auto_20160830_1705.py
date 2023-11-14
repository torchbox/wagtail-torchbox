# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-30 16:05


from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0054_auto_20160826_1657"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mainmenuitem",
            name="main_menu",
        ),
        migrations.RemoveField(
            model_name="mainmenuitem",
            name="page",
        ),
        migrations.AddField(
            model_name="mainmenu",
            name="menu",
            field=wagtail.fields.StreamField(
                [
                    (
                        b"items",
                        wagtail.blocks.StructBlock(
                            [
                                (b"page", wagtail.blocks.PageChooserBlock()),
                                (
                                    b"subitems",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                b"subitem",
                                                wagtail.blocks.PageChooserBlock(),
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
        migrations.DeleteModel(
            name="MainMenuItem",
        ),
    ]
