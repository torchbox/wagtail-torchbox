# Generated by Django 2.2.17 on 2021-08-02 14:40

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0137_auto_20210802_1445"),
    ]

    operations = [
        migrations.AlterField(
            model_name="globalsettings",
            name="addresses",
            field=wagtail.fields.StreamField(
                [
                    (
                        "address",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(blank=True)),
                                ("address", wagtail.blocks.RichTextBlock(blank=True),),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
    ]
