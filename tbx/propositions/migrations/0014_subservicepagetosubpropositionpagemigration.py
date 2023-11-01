# Generated by Django 3.2.18 on 2023-08-30 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0042_add_social_fields_to_all_page_types"),
        ("propositions", "0013_alter_subpropositionpage_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubServicePageToSubPropositionPageMigration",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "subservice_page_was_live",
                    models.BooleanField(default=True, editable=False),
                ),
                (
                    "subproposition_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="propositions.subpropositionpage",
                    ),
                ),
                (
                    "subservice_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="services.subservicepage",
                    ),
                ),
            ],
        ),
    ]
