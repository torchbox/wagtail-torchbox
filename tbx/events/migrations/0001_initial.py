# Generated by Django 2.2.17 on 2021-06-22 15:25

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taxonomy", "0005_service_contact_reasons"),
        ("people", "0024_auto_20210412_1428"),
        ("wagtailcore", "0062_comment_models_and_pagesubscription"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventIndexPage",
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
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="Event",
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
                ("title", models.CharField(max_length=255)),
                ("intro", models.TextField(verbose_name="Description")),
                ("link_external", models.URLField(verbose_name="External link")),
                ("date", models.DateField(verbose_name="Event date")),
                ("event_type", models.CharField(max_length=30)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="authors",
                        to="people.Author",
                        verbose_name="Host",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="events.EventIndexPage",
                    ),
                ),
                (
                    "related_services",
                    modelcluster.fields.ParentalManyToManyField(
                        related_name="events", to="taxonomy.Service"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
    ]