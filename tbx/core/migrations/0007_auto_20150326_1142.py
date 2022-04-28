# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0006_auto_20150326_1023"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.RichTextField(
                verbose_name="body (deprecated. Use streamfield instead)", blank=True
            ),
            preserve_default=True,
        ),
    ]
