# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-18 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields

from tbx.core.utils.migrations import for_each_page_revision


def update_contenttypes(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    ContentType = apps.get_model("contenttypes.ContentType")

    person_index_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="personindexpage"
    )
    person_index_next, created = ContentType.objects.get_or_create(
        app_label="people", model="personindexpage"
    )
    person_page_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="personpage"
    )
    person_page_next, created = ContentType.objects.get_or_create(
        app_label="people", model="personpage"
    )

    Page.objects.filter(content_type=person_index_prev).update(
        content_type=person_index_next
    )
    Page.objects.filter(content_type=person_page_prev).update(
        content_type=person_page_next
    )

    person_index_prev.delete()
    person_page_prev.delete()


def reverse_update_contenttypes(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    ContentType = apps.get_model("contenttypes.ContentType")

    person_index_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="personindexpage"
    )
    person_index_next, created = ContentType.objects.get_or_create(
        app_label="people", model="personindexpage"
    )
    person_page_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="personpage"
    )
    person_page_next, created = ContentType.objects.get_or_create(
        app_label="people", model="personpage"
    )

    Page.objects.filter(content_type=person_index_next).update(
        content_type=person_index_prev
    )
    Page.objects.filter(content_type=person_page_next).update(
        content_type=person_page_prev
    )

    person_index_next.delete()
    person_page_next.delete()


# Update the content types in revisions or django-modelcluster will crash when trying to deserialise
@for_each_page_revision("people.PersonIndexPage", "people.PersonPage")
def update_content_type_in_revisions(page, revision_content):
    revision_content["content_type"] = page.content_type_id
    return revision_content


def nooperation(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtaildocs", "0008_document_file_size"),
        ("torchbox", "0112_move_people_into_new_app"),
        ("wagtailcore", "0040_page_draft_title"),
    ]

    state_operations = [
        migrations.CreateModel(
            name="PersonIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("intro", models.TextField()),
                ("senior_management_intro", models.TextField()),
                ("team_intro", models.TextField()),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PersonPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("telephone", models.CharField(blank=True, max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("address_1", models.CharField(blank=True, max_length=255)),
                ("address_2", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=255)),
                ("country", models.CharField(blank=True, max_length=255)),
                ("post_code", models.CharField(blank=True, max_length=10)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("role", models.CharField(blank=True, max_length=255)),
                ("is_senior", models.BooleanField(default=False)),
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("biography", wagtail.fields.RichTextField(blank=True)),
                (
                    "short_biography",
                    models.CharField(
                        blank=True,
                        help_text="A shorter summary biography for including in other pages",
                        max_length=255,
                    ),
                ),
                (
                    "feed_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="torchbox.TorchboxImage",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="torchbox.TorchboxImage",
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="PersonPageRelatedLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "link_external",
                    models.URLField(blank=True, verbose_name="External link"),
                ),
                ("title", models.CharField(help_text="Link title", max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtaildocs.Document",
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_links",
                        to="people.PersonPage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations, database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[],
            database_operations=[
                migrations.RunPython(nooperation, update_content_type_in_revisions),
                migrations.RunPython(update_contenttypes, reverse_update_contenttypes),
                migrations.RunPython(update_content_type_in_revisions, nooperation),
            ],
        ),
    ]
