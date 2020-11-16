# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-22 12:00
from __future__ import unicode_literals

import json
from functools import wraps

from django.db import migrations

from tbx.core.utils.migrations import for_each_page_revision


@for_each_page_revision("work.WorkPage")
def rename_streamfield_to_body_in_revisions(page, content):
    # Not all revisions have the 'streamfield' key
    if "streamfield" in content:
        content["old_body"] = content["body"]
        content["body"] = content["streamfield"]
        del content["streamfield"]

    return content


@for_each_page_revision("work.WorkPage")
def unrename_streamfield_to_body_in_revisions(page, content):
    # Not all revisions had the 'streamfield' key. So they weren't migrated in the first place
    if "old_body" in content:
        content["streamfield"] = content["body"]
        content["body"] = content["old_body"]
        del content["old_body"]

    return content


class Migration(migrations.Migration):

    dependencies = [
        ("work", "0009_remove_play_fields"),
    ]

    operations = [
        migrations.RunPython(
            rename_streamfield_to_body_in_revisions,
            unrename_streamfield_to_body_in_revisions,
        ),
        migrations.RenameField(
            model_name="workpage", old_name="streamfield", new_name="body",
        ),
    ]
