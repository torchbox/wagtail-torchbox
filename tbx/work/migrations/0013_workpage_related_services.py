# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-22 15:10
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("taxonomy", "0001_initial"),
        ("work", "0012_remove_workpage_intro"),
    ]

    operations = [
        migrations.AddField(
            model_name="workpage",
            name="related_services",
            field=modelcluster.fields.ParentalManyToManyField(
                related_name="case_studies", to="taxonomy.Service"
            ),
        ),
    ]
