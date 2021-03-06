# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-21 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0115_delete_tshirt_page"),
        ("people", "0004_auto_20190123_1133"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                ("role", models.CharField(blank=True, max_length=255)),
                ("email_address", models.EmailField(max_length=254)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(max_length=128),
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
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
