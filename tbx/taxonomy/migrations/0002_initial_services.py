# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-16 11:15
from __future__ import unicode_literals

from django.db import migrations
from django.utils.text import slugify


def insert_initial_services(apps, schema_editor):
    Service = apps.get_model("taxonomy.Service")

    def add_service(order, name, slug=None):
        if slug is None:
            slug = slugify(name)

        Service.objects.create(
            name=name, slug=slug, sort_order=order,
        )

    add_service(100, "Digital products")
    add_service(200, "Wagtail")
    add_service(300, "Digital Marketing")
    add_service(400, "PPC")
    add_service(500, "SEO")
    add_service(600, "Social media")
    add_service(700, "Data")
    add_service(800, "Google Ad Grants")


def nooperation(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("taxonomy", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insert_initial_services, nooperation),
    ]
