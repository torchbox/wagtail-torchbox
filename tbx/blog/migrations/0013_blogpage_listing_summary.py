# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-22 13:12
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.db import migrations, models


def migrate_intro_to_listing_summary(apps, schema_editor):
    BlogPage = apps.get_model("blog.BlogPage")

    for blog_page in BlogPage.objects.all():
        if blog_page.intro not in ["", "<p></p>", "<p><br/><p>"]:
            # No blog posts use any rich text features in the intro field
            blog_page.listing_summary = BeautifulSoup(
                blog_page.intro, "html.parser"
            ).get_text()

            blog_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0012_remove_blogpage_marketing_only"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="listing_summary",
            field=models.TextField(blank=True),
        ),
        migrations.RunPython(migrate_intro_to_listing_summary),
    ]
