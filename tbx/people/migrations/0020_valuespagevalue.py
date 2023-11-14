# Generated by Django 2.2.17 on 2021-04-09 15:45

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0019_valuespage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ValuesPageValue",
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
                ("heading", wagtail.fields.RichTextField(blank=True)),
                ("text", models.CharField(max_length=255)),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="values",
                        to="people.ValuesPage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]
