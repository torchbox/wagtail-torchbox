# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-21 13:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0113_move_people_into_new_app_2"),
    ]

    operations = [
        migrations.RemoveField(model_name="standardpage", name="show_in_play_menu",),
    ]
