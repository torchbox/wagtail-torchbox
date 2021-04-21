# Generated by Django 2.2.17 on 2021-04-21 04:29

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0023_merge_20210330_1437"),
    ]

    operations = [
        migrations.AddField(
            model_name="culturepage",
            name="instagram_posts",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "posts",
                        wagtail.core.blocks.StreamBlock(
                            [("post", wagtail.embeds.blocks.EmbedBlock())],
                            max_num=8,
                            min_num=8,
                            required=False,
                            template="patterns/molecules/instagram-gallery/instagram-gallery.html",
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
