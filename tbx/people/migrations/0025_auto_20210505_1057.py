# Generated by Django 2.2.17 on 2021-05-05 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0024_auto_20210416_1406"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="culturepage",
            name="body",
        ),
        migrations.RemoveField(
            model_name="culturepage",
            name="contact",
        ),
        migrations.RemoveField(
            model_name="culturepage",
            name="strapline_visible",
        ),
    ]
