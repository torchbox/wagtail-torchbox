# Generated by Django 2.2.12 on 2020-08-13 14:33

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0126_jobindexpage_jobs_xml_feed"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobindexpage",
            name="intro",
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
