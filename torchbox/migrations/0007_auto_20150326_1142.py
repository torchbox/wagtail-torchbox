# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0006_auto_20150326_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(verbose_name='body (deprecated. Use streamfield instead)', blank=True),
            preserve_default=True,
        ),
    ]
