# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0013_auto_20150720_1154"),
    ]

    operations = [
        migrations.AddField(
            model_name="workpage",
            name="show_in_play_menu",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
