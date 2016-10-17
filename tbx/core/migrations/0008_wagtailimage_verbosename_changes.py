# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0007_auto_20150326_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torchboximage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torchboximage',
            name='height',
            field=models.IntegerField(verbose_name='Height', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torchboximage',
            name='uploaded_by_user',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Uploaded by user'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torchboximage',
            name='width',
            field=models.IntegerField(verbose_name='Width', editable=False),
            preserve_default=True,
        ),
    ]
