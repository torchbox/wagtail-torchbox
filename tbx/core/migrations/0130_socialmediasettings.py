# Generated by Django 2.2.13 on 2020-10-22 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0052_pagelogentry"),
        ("torchbox", "0129_auto_20201007_1514"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialMediaSettings",
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
                    "twitter_handle",
                    models.CharField(
                        blank=True,
                        help_text="Your Twitter username without the @, e.g. katyperry",
                        max_length=255,
                    ),
                ),
                (
                    "facebook_app_id",
                    models.CharField(
                        blank=True, help_text="Your Facebook app ID.", max_length=255
                    ),
                ),
                (
                    "default_sharing_text",
                    models.CharField(
                        blank=True,
                        help_text="Default sharing text to use if social text has not been set on a page.",
                        max_length=255,
                    ),
                ),
                (
                    "site_name",
                    models.CharField(
                        blank=True,
                        default="{{ cookiecutter.project_name }}",
                        help_text="Site name, used by Open Graph.",
                        max_length=255,
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
