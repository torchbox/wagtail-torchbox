# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.images.models
import django.db.models.deletion
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0014_workpage_show_in_play_menu"),
    ]

    operations = [
        migrations.AddField(
            model_name="torchboximage",
            name="file_size",
            field=models.PositiveIntegerField(null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="created at", db_index=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="file",
            field=models.ImageField(
                height_field="height",
                upload_to=wagtail.images.models.get_upload_to,
                width_field="width",
                verbose_name="file",
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="height",
            field=models.IntegerField(verbose_name="height", editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="tags",
            field=taggit.managers.TaggableManager(
                to="taggit.Tag",
                through="taggit.TaggedItem",
                blank=True,
                help_text=None,
                verbose_name="tags",
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="title",
            field=models.CharField(max_length=255, verbose_name="title"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="uploaded_by_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
                verbose_name="uploaded by user",
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="torchboximage",
            name="width",
            field=models.IntegerField(verbose_name="width", editable=False),
            preserve_default=True,
        ),
    ]
