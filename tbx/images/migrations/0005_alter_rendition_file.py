# Generated by Django 4.2 on 2023-12-12 10:39

from django.db import migrations
import wagtail.images.models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0004_wagtail42_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rendition",
            name="file",
            field=wagtail.images.models.WagtailImageField(
                height_field="height",
                storage=wagtail.images.models.get_rendition_storage,
                upload_to=wagtail.images.models.get_rendition_upload_to,
                width_field="width",
            ),
        ),
    ]
