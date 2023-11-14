# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-22 13:23
from __future__ import unicode_literals

import json
from functools import wraps
from uuid import UUID, uuid3

from django.db import migrations

from wagtail.blocks import StreamValue
from wagtail.rich_text import RichText

from tbx.core.utils.migrations import for_each_page_revision


UUID_NAMESPACE = UUID("eac1f6e4-1d92-468f-8896-37086343ae0d")


def migrate_standardpage_intro_and_body_to_streamfield(apps, schema_editor):
    StandardPage = apps.get_model("torchbox.StandardPage")
    stream_block = StandardPage._meta.get_field("streamfield").stream_block

    # Append body to beginning of streamfield
    for page in StandardPage.objects.exclude(body__in=["", "<p></p>", "<p><br/></p>"]):
        # Add body as first block so it appears in the same place on the template
        page.streamfield = StreamValue(
            stream_block,
            [
                (
                    "paragraph",
                    RichText(page.body),
                    str(uuid3(UUID_NAMESPACE, page.body)),
                ),
            ]
            + [(child.block_type, child.value, child.id) for child in page.streamfield],
        )

        page.save()

    # Append intro to beginning of streamfield
    for page in StandardPage.objects.exclude(intro__in=["", "<p></p>", "<p><br/></p>"]):
        # Add intro as first block so it appears in the same place on the template
        page.streamfield = StreamValue(
            stream_block,
            [
                (
                    "paragraph",
                    RichText(page.intro),
                    str(uuid3(UUID_NAMESPACE, page.intro)),
                ),
            ]
            + [(child.block_type, child.value, child.id) for child in page.streamfield],
        )

        page.save()


def nooperation(apps, schema_editor):
    pass


@for_each_page_revision("torchbox.StandardPage")
def update_revisions(page, content):
    streamfield_json = content.get("streamfield", "")

    if streamfield_json:
        streamfield = json.loads(streamfield_json)
    else:
        streamfield = []

    # Append body to beginning of streamfield
    if content["body"] not in ["", "<p></p>", "<p><br/></p>"]:
        content["old_body"] = content["body"]

        streamfield.insert(
            0,
            {
                "type": "paragraph",
                "value": content["body"],
                "id": str(uuid3(UUID_NAMESPACE, content["body"])),
            },
        )

    # Append intro to beginning of streamfield
    if content["intro"] not in ["", "<p></p>", "<p><br/></p>"]:
        streamfield.insert(
            0,
            {
                "type": "paragraph",
                "value": content["intro"],
                "id": str(uuid3(UUID_NAMESPACE, content["intro"])),
            },
        )

    # Save streamfield content with "body" key, as it was renamed as well in this migration
    content["body"] = json.dumps(streamfield)

    return content


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0117_remove_standardpage_middle_break"),
    ]

    operations = [
        migrations.RunPython(
            migrate_standardpage_intro_and_body_to_streamfield, nooperation
        ),
        migrations.RemoveField(
            model_name="standardpage",
            name="body",
        ),
        migrations.RemoveField(
            model_name="standardpage",
            name="intro",
        ),
        migrations.RenameField(
            model_name="standardpage",
            old_name="streamfield",
            new_name="body",
        ),
        migrations.RunPython(update_revisions),
    ]
