# Generated by Django 2.1.5 on 2019-01-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0005_contact"),
    ]

    operations = [
        migrations.RemoveField(model_name="personindexpage", name="intro",),
        migrations.RemoveField(
            model_name="personindexpage", name="senior_management_intro",
        ),
        migrations.RemoveField(model_name="personindexpage", name="team_intro",),
        migrations.AddField(
            model_name="personindexpage",
            name="strapline",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]
