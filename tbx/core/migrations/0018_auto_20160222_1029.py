# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 10:29


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0017_merge"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="googleadgrantsaccreditations",
            options={"ordering": ["sort_order"]},
        ),
        migrations.AlterModelOptions(
            name="googleadgrantspagequote",
            options={"ordering": ["sort_order"]},
        ),
        migrations.AddField(
            model_name="googleadgrantsaccreditations",
            name="sort_order",
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="googleadgrantspagequote",
            name="sort_order",
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="googleadgrantapplication",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="personpage",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
