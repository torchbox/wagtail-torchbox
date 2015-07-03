# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0011_auto_20150612_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkPageAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('author', models.ForeignKey(related_name='+', blank=True, to='torchbox.PersonPage', null=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='related_author', to='torchbox.WorkPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workpage',
            name='author_left',
            field=models.CharField(help_text='author who has left Torchbox', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
