# Generated by Django 2.2.17 on 2021-03-26 14:04

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0021_rename_benefits_on_culturepage_model_"),
    ]

    operations = [
        migrations.AddField(
            model_name="culturepage",
            name="blogs_section_title",
            field=models.CharField(blank=True, max_length=100, verbose_name="Title"),
        ),
        migrations.AddField(
            model_name="culturepage",
            name="featured_blog_posts",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "blog_post",
                        wagtail.core.blocks.PageChooserBlock(
                            page_type=["blog.BlogPage"]
                        ),
                    )
                ],
                blank=True,
                verbose_name="Blog posts",
            ),
        ),
    ]