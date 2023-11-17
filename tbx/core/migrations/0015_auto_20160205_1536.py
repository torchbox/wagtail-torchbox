# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0001_squashed_0016_change_page_url_path_to_text_field"),
        ("torchbox", "0014_workpage_show_in_play_menu"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoogleAdGrantApplication",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=75)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="GoogleAdGrantsAccreditations",
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
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="torchbox.TorchboxImage",
                        null=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="GoogleAdGrantsPage",
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
                ("intro", wagtail.fields.RichTextField()),
                ("form_title", models.CharField(max_length=255)),
                ("form_subtitle", models.CharField(max_length=255)),
                ("form_button_text", models.CharField(max_length=255)),
                ("body", wagtail.fields.RichTextField()),
                ("grants_managed_title", models.CharField(max_length=255)),
                ("call_to_action_title", models.CharField(max_length=255)),
                ("call_to_action_embed_url", models.URLField()),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="GoogleAdGrantsPageGrantsManaged",
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
                        related_name="grants_managed", to="torchbox.GoogleAdGrantsPage"
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="GoogleAdGrantsPageQuote",
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
                ("text", models.TextField()),
                ("person_name", models.CharField(max_length=255)),
                ("organisation_name", models.CharField(max_length=255)),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="quotes", to="torchbox.GoogleAdGrantsPage"
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="googleadgrantsaccreditations",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="accreditations", to="torchbox.GoogleAdGrantsPage"
            ),
            preserve_default=True,
        ),
    ]
