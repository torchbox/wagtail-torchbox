# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0008_wagtailimage_verbosename_changes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="intro",
            field=wagtail.fields.RichTextField(
                verbose_name="Intro (used only for blog index listing)", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="height",
            field=models.IntegerField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="uploaded_by_user",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="width",
            field=models.IntegerField(editable=False),
            preserve_default=True,
        ),
    ]
