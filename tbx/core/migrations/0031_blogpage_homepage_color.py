# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-17 11:40


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0030_auto_20160617_1146"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="homepage_color",
            field=models.TextField(
                blank=True,
                verbose_name="Homepage colour (orange, blue, white) if left blank will display image",
            ),
        ),
    ]
