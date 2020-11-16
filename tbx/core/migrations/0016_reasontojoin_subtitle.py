# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0015_auto_20151105_1715"),
    ]

    operations = [
        migrations.AddField(
            model_name="reasontojoin",
            name="subtitle",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]
