# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import tbx.core.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtailmarkdown.blocks

from tbx.core.utils.migrations import for_each_page_revision


def update_contenttypes(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    ContentType = apps.get_model("contenttypes.ContentType")

    work_index_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="workindexpage"
    )
    work_index_next, created = ContentType.objects.get_or_create(
        app_label="work", model="workindexpage"
    )
    work_page_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="workpage"
    )
    work_page_next, created = ContentType.objects.get_or_create(
        app_label="work", model="workpage"
    )

    Page.objects.filter(content_type=work_index_prev).update(
        content_type=work_index_next
    )
    Page.objects.filter(content_type=work_page_prev).update(content_type=work_page_next)

    work_index_prev.delete()
    work_page_prev.delete()


def reverse_update_contenttypes(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    ContentType = apps.get_model("contenttypes.ContentType")

    work_index_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="workindexpage"
    )
    work_index_next, created = ContentType.objects.get_or_create(
        app_label="work", model="workindexpage"
    )
    work_page_prev, created = ContentType.objects.get_or_create(
        app_label="torchbox", model="workpage"
    )
    work_page_next, created = ContentType.objects.get_or_create(
        app_label="work", model="workpage"
    )

    Page.objects.filter(content_type=work_index_next).update(
        content_type=work_index_prev
    )
    Page.objects.filter(content_type=work_page_next).update(content_type=work_page_prev)

    work_index_next.delete()
    work_page_next.delete()


# Update the content types in revisions or django-modelcluster will crash when trying to deserialise
@for_each_page_revision("work.WorkIndexPage", "work.WorkPage")
def update_content_type_in_revisions(page, revision_content):
    revision_content["content_type"] = page.content_type_id
    return revision_content


def nooperation(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0040_page_draft_title"),
        ("torchbox", "0108_move_work_into_new_app"),
    ]

    run_before = [
        ("torchbox", "0110_rename_blogpagetaglist_to_tag"),
    ]

    state_operations = [
        migrations.CreateModel(
            name="WorkIndexPage",
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
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("show_in_play_menu", models.BooleanField(default=False)),
                ("hide_popular_tags", models.BooleanField(default=False)),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="WorkPage",
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
                (
                    "author_left",
                    models.CharField(
                        blank=True,
                        help_text="author who has left Torchbox",
                        max_length=255,
                    ),
                ),
                ("summary", models.CharField(max_length=255)),
                ("descriptive_title", models.CharField(max_length=255)),
                (
                    "intro",
                    wagtail.fields.RichTextField(
                        blank=True,
                        verbose_name="Intro (deprecated. Use streamfield instead)",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.RichTextField(
                        blank=True,
                        verbose_name="Body (deprecated. Use streamfield instead)",
                    ),
                ),
                (
                    "marketing_only",
                    models.BooleanField(
                        default=False,
                        help_text="Display this work item only on marketing landing page",
                    ),
                ),
                (
                    "streamfield",
                    wagtail.fields.StreamField(
                        [
                            (
                                "h2",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "h3",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "h4",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow"),),
                            (
                                "paragraph",
                                wagtail.blocks.RichTextBlock(icon="pilcrow"),
                            ),
                            (
                                "aligned_image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "alignment",
                                            tbx.core.blocks.ImageFormatChoiceBlock(),
                                        ),
                                        ("caption", wagtail.blocks.CharBlock()),
                                        (
                                            "attribution",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                    ],
                                    label="Aligned image",
                                ),
                            ),
                            (
                                "wide_image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        )
                                    ],
                                    label="Wide image",
                                ),
                            ),
                            (
                                "bustout",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        ("text", wagtail.blocks.RichTextBlock()),
                                    ]
                                ),
                            ),
                            (
                                "pullquote",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "quote",
                                            wagtail.blocks.CharBlock(
                                                classname="quote title"
                                            ),
                                        ),
                                        ("attribution", wagtail.blocks.CharBlock(),),
                                    ]
                                ),
                            ),
                            (
                                "raw_html",
                                wagtail.blocks.RawHTMLBlock(
                                    icon="code", label="Raw HTML"
                                ),
                            ),
                            ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                            (
                                "markdown",
                                wagtailmarkdown.blocks.MarkdownBlock(icon="code"),
                            ),
                        ]
                    ),
                ),
                ("visit_the_site", models.URLField(blank=True)),
                ("show_in_play_menu", models.BooleanField(default=False)),
                (
                    "feed_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image used on listings and social media.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.Image",
                    ),
                ),
                (
                    "homepage_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.Image",
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="WorkPageAuthor",
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
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="torchbox.PersonPage",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_author",
                        to="work.WorkPage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
        migrations.CreateModel(
            name="WorkPageScreenshot",
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
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.Image",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="screenshots",
                        to="work.WorkPage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
        migrations.CreateModel(
            name="WorkPageTagSelect",
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
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="work.WorkPage",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="work_page_tag_select",
                        to="torchbox.BlogPageTagList",
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
