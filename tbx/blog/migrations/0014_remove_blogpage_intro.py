# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-22 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_blogpage_listing_summary"),
    ]

    operations = [
        migrations.RemoveField(model_name="blogpage", name="intro",),
    ]
