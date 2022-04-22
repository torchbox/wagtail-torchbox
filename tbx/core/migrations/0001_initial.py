# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.images.models
import wagtail.fields
import wagtail.search.index
import modelcluster.fields
import django.db.models.deletion
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0005_make_filter_spec_unique"),
        ("taggit", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailcore", "0010_change_page_owner_to_null_on_delete"),
        ("wagtaildocs", "0002_initial_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="Advert",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("url", models.URLField(null=True, blank=True)),
                ("text", models.CharField(max_length=255)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="AdvertPlacement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "advert",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="torchbox.Advert",
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogIndexPage",
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
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="BlogIndexPageRelatedLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(verbose_name=b"External link", blank=True),
                ),
                ("title", models.CharField(help_text=b"Link title", max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPage",
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
                ("body", wagtail.fields.RichTextField()),
                (
                    "author_left",
                    models.CharField(
                        help_text=b"author who has left Torchbox",
                        max_length=255,
                        blank=True,
                    ),
                ),
                ("date", models.DateField(verbose_name=b"Post date")),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="BlogPageAuthor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPageRelatedLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(verbose_name=b"External link", blank=True),
                ),
                ("title", models.CharField(help_text=b"Link title", max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPageTagList",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.CharField(max_length=255)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPageTagSelect",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="tags", to="torchbox.BlogPage"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        related_name="blog_page_tag_select",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="torchbox.BlogPageTagList",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="HomePage",
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
                ("intro", models.TextField(blank=True)),
                (
                    "hero_video_id",
                    models.IntegerField(
                        help_text=b"Optional. The numeric ID of a Vimeo video to replace the background image.",
                        null=True,
                        blank=True,
                    ),
                ),
            ],
            options={"verbose_name": "Homepage",},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="JobIndexPage",
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
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="JobIndexPageContentBlock",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                ("content", wagtail.fields.RichTextField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="content_block", to="torchbox.JobIndexPage"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="JobIndexPageJob",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                ("job_title", models.CharField(max_length=255)),
                ("url", models.URLField(null=True)),
                ("location", models.CharField(max_length=255, blank=True)),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="job", to="torchbox.JobIndexPage"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
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
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("show_in_play_menu", models.BooleanField(default=False)),
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
                ("telephone", models.CharField(max_length=20, blank=True)),
                ("email", models.EmailField(max_length=75, blank=True)),
                ("address_1", models.CharField(max_length=255, blank=True)),
                ("address_2", models.CharField(max_length=255, blank=True)),
                ("city", models.CharField(max_length=255, blank=True)),
                ("country", models.CharField(max_length=255, blank=True)),
                ("post_code", models.CharField(max_length=10, blank=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("role", models.CharField(max_length=255, blank=True)),
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("biography", wagtail.fields.RichTextField(blank=True)),
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
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(verbose_name=b"External link", blank=True),
                ),
                ("title", models.CharField(help_text=b"Link title", max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ServicesPage",
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
                ("body", wagtail.fields.RichTextField(blank=True)),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="ServicesPageContentBlock",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                ("content", wagtail.fields.RichTextField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="content_block", to="torchbox.ServicesPage"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ServicesPageRelatedLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(verbose_name=b"External link", blank=True),
                ),
                ("title", models.CharField(help_text=b"Link title", max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtaildocs.Document",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="StandardPage",
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
                ("credit", models.CharField(max_length=255, blank=True)),
                ("heading", wagtail.fields.RichTextField(blank=True)),
                ("quote", models.CharField(max_length=255, blank=True)),
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("middle_break", wagtail.fields.RichTextField(blank=True)),
                ("body", wagtail.fields.RichTextField(blank=True)),
                ("email", models.EmailField(max_length=75, blank=True)),
                ("show_in_play_menu", models.BooleanField(default=False)),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="StandardPageClients",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(verbose_name=b"External link", blank=True),
                ),
                ("title", models.CharField(help_text=b"Link title", max_length=255)),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="StandardPageContentBlock",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                ("content", wagtail.fields.RichTextField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="content_block", to="torchbox.StandardPage"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="StandardPageRelatedLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(verbose_name=b"External link", blank=True),
                ),
                ("title", models.CharField(help_text=b"Link title", max_length=255)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtaildocs.Document",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="TorchboxImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "file",
                    models.ImageField(
                        height_field="height",
                        upload_to=wagtail.images.models.get_upload_to,
                        width_field="width",
                        verbose_name="File",
                    ),
                ),
                ("width", models.IntegerField(editable=False)),
                ("height", models.IntegerField(editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("focal_point_x", models.PositiveIntegerField(null=True, blank=True)),
                ("focal_point_y", models.PositiveIntegerField(null=True, blank=True)),
                (
                    "focal_point_width",
                    models.PositiveIntegerField(null=True, blank=True),
                ),
                (
                    "focal_point_height",
                    models.PositiveIntegerField(null=True, blank=True),
                ),
                ("credit", models.CharField(max_length=255, blank=True)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        to="taggit.Tag",
                        through="taggit.TaggedItem",
                        blank=True,
                        help_text=None,
                        verbose_name="Tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name="TorchboxRendition",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        height_field="height", width_field="width", upload_to="images"
                    ),
                ),
                ("width", models.IntegerField(editable=False)),
                ("height", models.IntegerField(editable=False)),
                (
                    "focal_point_key",
                    models.CharField(
                        default="", max_length=255, editable=False, blank=True
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        related_name="renditions",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="torchbox.TorchboxImage",
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="TshirtPage",
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
                    "main_image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="torchbox.TorchboxImage",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
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
                ("summary", models.CharField(max_length=255)),
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("body", wagtail.fields.RichTextField(blank=True)),
                (
                    "homepage_image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="torchbox.TorchboxImage",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="WorkPageScreenshot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="torchbox.TorchboxImage",
                        null=True,
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="screenshots", to="torchbox.WorkPage"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="WorkPageTagSelect",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="tags", to="torchbox.WorkPage"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        related_name="work_page_tag_select",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="torchbox.BlogPageTagList",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="torchboxrendition",
            unique_together=set([("image", "focal_point_key")]),
        ),
        migrations.AddField(
            model_name="standardpagerelatedlink",
            name="link_page",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpagerelatedlink",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="related_links", to="torchbox.StandardPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpageclients",
            name="image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpageclients",
            name="link_document",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="wagtaildocs.Document",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpageclients",
            name="link_page",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpageclients",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="clients", to="torchbox.StandardPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpage",
            name="feed_image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="standardpage",
            name="main_image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="servicespagerelatedlink",
            name="link_page",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="servicespagerelatedlink",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="related_links", to="torchbox.ServicesPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="servicespage",
            name="feed_image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personpagerelatedlink",
            name="link_page",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personpagerelatedlink",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="related_links", to="torchbox.PersonPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personpage",
            name="feed_image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personpage",
            name="image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_video_poster_image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogpagerelatedlink",
            name="link_page",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogpagerelatedlink",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="related_links", to="torchbox.BlogPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogpageauthor",
            name="author",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="torchbox.PersonPage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogpageauthor",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="related_author", to="torchbox.BlogPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogpage",
            name="feed_image",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="torchbox.TorchboxImage",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogindexpagerelatedlink",
            name="link_page",
            field=models.ForeignKey(
                related_name="+",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogindexpagerelatedlink",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="related_links", to="torchbox.BlogIndexPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="advertplacement",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="advert_placements", to="wagtailcore.Page"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="advert",
            name="page",
            field=models.ForeignKey(
                related_name="adverts",
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.Page",
                null=True,
            ),
            preserve_default=True,
        ),
    ]
