# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks

from tbx.core.utils.migrations import for_each_page_revision


def update_contenttypes(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    ContentType = apps.get_model("contenttypes.ContentType")

    service_index_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="servicespage"
    )
    service_index_next, created = ContentType.objects.get_or_create(
        app_label="services", model="serviceindexpage"
    )
    service_page_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="servicepage"
    )
    service_page_next, created = ContentType.objects.get_or_create(
        app_label="services", model="servicepage"
    )

    Page.objects.filter(content_type=service_index_prev).update(
        content_type=service_index_next
    )
    Page.objects.filter(content_type=service_page_prev).update(
        content_type=service_page_next
    )

    service_index_prev.delete()
    service_page_prev.delete()


def reverse_update_contenttypes(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    ContentType = apps.get_model("contenttypes.ContentType")

    service_index_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="servicespage"
    )
    service_index_next, created = ContentType.objects.get_or_create(
        app_label="services", model="serviceindexpage"
    )
    service_page_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="servicepage"
    )
    service_page_next, created = ContentType.objects.get_or_create(
        app_label="services", model="servicepage"
    )

    Page.objects.filter(content_type=service_index_next).update(
        content_type=service_index_prev
    )
    Page.objects.filter(content_type=service_page_next).update(
        content_type=service_page_prev
    )

    service_index_next.delete()
    service_page_next.delete()


# Update the content types in revisions or django-modelcluster will crash when trying to deserialise
@for_each_page_revision("services.ServiceIndexPage", "services.ServicePage")
def update_content_type_in_revisions(page, revision_content):
    revision_content["content_type"] = page.content_type_id
    return revision_content


def nooperation(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0040_page_draft_title"),
        ("torchbox", "0107_move_services_into_new_app"),
    ]

    state_operations = [
        migrations.CreateModel(
            name="ServicePage",
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
                ("description", models.TextField()),
                (
                    "streamfield",
                    wagtail.fields.StreamField(
                        [
                            (
                                "paragraph",
                                wagtail.blocks.RichTextBlock(icon="pilcrow"),
                            ),
                            (
                                "case_studies",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(required=True),
                                        ),
                                        (
                                            "intro",
                                            wagtail.blocks.TextBlock(required=True),
                                        ),
                                        (
                                            "case_studies",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "page",
                                                            wagtail.blocks.PageChooserBlock(
                                                                "work.WorkPage"
                                                            ),
                                                        ),
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "descriptive_title",
                                                            wagtail.blocks.CharBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "highlights",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(required=True),
                                        ),
                                        (
                                            "intro",
                                            wagtail.blocks.RichTextBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            "highlights",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.TextBlock()
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "pull_quote",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "quote",
                                            wagtail.blocks.CharBlock(
                                                classname="quote title"
                                            ),
                                        ),
                                        (
                                            "attribution",
                                            wagtail.blocks.CharBlock(),
                                        ),
                                    ],
                                    template="blocks/services/pull_quote_block.html",
                                ),
                            ),
                            (
                                "process",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(required=True),
                                        ),
                                        (
                                            "intro",
                                            wagtail.blocks.TextBlock(required=False),
                                        ),
                                        (
                                            "steps",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "subtitle",
                                                            wagtail.blocks.CharBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(
                                                                required=True
                                                            ),
                                                        ),
                                                        (
                                                            "icon",
                                                            wagtail.blocks.CharBlock(
                                                                help_text="Paste SVG code here",
                                                                max_length=9000,
                                                                required=True,
                                                            ),
                                                        ),
                                                        (
                                                            "description",
                                                            wagtail.blocks.RichTextBlock(
                                                                required=True
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "people",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(required=True),
                                        ),
                                        (
                                            "intro",
                                            wagtail.blocks.RichTextBlock(required=True),
                                        ),
                                        (
                                            "people",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.PageChooserBlock()
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "featured_pages",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("title", wagtail.blocks.CharBlock()),
                                        (
                                            "pages",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "page",
                                                            wagtail.blocks.PageChooserBlock(),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(),
                                                        ),
                                                        (
                                                            "text",
                                                            wagtail.blocks.TextBlock(),
                                                        ),
                                                        (
                                                            "sub_text",
                                                            wagtail.blocks.CharBlock(
                                                                max_length=100
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "sign_up_form_page",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "page",
                                            wagtail.blocks.PageChooserBlock(
                                                "sign_up_form.SignUpFormPage"
                                            ),
                                        )
                                    ]
                                ),
                            ),
                            (
                                "logos",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("title", wagtail.blocks.CharBlock()),
                                        ("intro", wagtail.blocks.CharBlock()),
                                        (
                                            "logos",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(),
                                                        ),
                                                        (
                                                            "link_page",
                                                            wagtail.blocks.PageChooserBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "link_external",
                                                            wagtail.blocks.URLBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                (
                    "particle",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="torchbox.ParticleSnippet",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="ServiceIndexPage",
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
                ("heading", models.TextField(blank=True)),
                ("intro", models.TextField(blank=True)),
                (
                    "main_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="torchbox.TorchboxImage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="ServiceIndexPageService",
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
                ("title", models.TextField()),
                ("svg", models.TextField(null=True)),
                ("description", models.TextField()),
                (
                    "link",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="services.ServicePage",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="services.ServiceIndexPage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
            database_operations=[],
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
