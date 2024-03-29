# Generated by Django 2.2.17 on 2021-03-11 13:05

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0018_update_contact"),
    ]

    operations = [
        migrations.AddField(
            model_name="culturepage",
            name="heading_for_key_points",
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name="culturepage",
            name="key_points_section_title",
            field=models.TextField(blank=True, default="Benefits"),
        ),
    ]
