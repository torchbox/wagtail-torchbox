# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0011_auto_20150507_1213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workpage',
            options={'ordering': ['-pk']},
        ),
    ]
