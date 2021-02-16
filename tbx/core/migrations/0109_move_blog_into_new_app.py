# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 21:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0040_page_draft_title"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("wagtailsearchpromotions", "0002_capitalizeverbose"),
        ("wagtailforms", "0003_capitalizeverbose"),
        ("work", "0001_initial"),
        ("torchbox", "0108_move_work_into_new_app"),
    ]

    database_operations = [
        migrations.AlterModelTable("BlogIndexPage", "blog_blogindexpage"),
        migrations.AlterModelTable(
            "BlogIndexPageRelatedLink", "blog_blogindexpagerelatedlink"
        ),
        migrations.AlterModelTable("BlogPage", "blog_blogpage"),
        migrations.AlterModelTable("BlogPageAuthor", "blog_blogpageauthor"),
        migrations.AlterModelTable("BlogPageRelatedLink", "blog_blogpagerelatedlink"),
        migrations.AlterModelTable("BlogPageTagSelect", "blog_blogpagetagselect"),
    ]

    state_operations = [
        migrations.RemoveField(model_name="blogindexpage", name="page_ptr",),
        migrations.RemoveField(
            model_name="blogindexpagerelatedlink", name="link_document",
        ),
        migrations.RemoveField(
            model_name="blogindexpagerelatedlink", name="link_page",
        ),
        migrations.RemoveField(model_name="blogindexpagerelatedlink", name="page",),
        migrations.RemoveField(model_name="blogpage", name="feed_image",),
        migrations.RemoveField(model_name="blogpage", name="page_ptr",),
        migrations.RemoveField(model_name="blogpageauthor", name="author",),
        migrations.RemoveField(model_name="blogpageauthor", name="page",),
        migrations.RemoveField(model_name="blogpagerelatedlink", name="link_document",),
        migrations.RemoveField(model_name="blogpagerelatedlink", name="link_page",),
        migrations.RemoveField(model_name="blogpagerelatedlink", name="page",),
        migrations.RemoveField(model_name="blogpagetagselect", name="page",),
        migrations.RemoveField(model_name="blogpagetagselect", name="tag",),
        migrations.DeleteModel(name="BlogIndexPage",),
        migrations.DeleteModel(name="BlogIndexPageRelatedLink",),
        migrations.DeleteModel(name="BlogPage",),
        migrations.DeleteModel(name="BlogPageAuthor",),
        migrations.DeleteModel(name="BlogPageRelatedLink",),
        migrations.DeleteModel(name="BlogPageTagSelect",),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations, state_operations=state_operations,
        )
    ]
