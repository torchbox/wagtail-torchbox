# Generated by Django 2.1.5 on 2019-03-16 16:41

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0011_auto_20190216_1748"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactReason",
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
                ("description", models.TextField()),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
        migrations.CreateModel(
            name="ContactReasonsList",
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
                ("name", models.CharField(blank=True, max_length=255)),
                ("heading", models.TextField()),
                (
                    "is_default",
                    models.BooleanField(
                        blank=True, default=False, null=True, unique=True
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="contactreason",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reasons",
                to="people.ContactReasonsList",
            ),
        ),
    ]
