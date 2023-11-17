# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0015_auto_20160205_1536"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="googleadgrantapplication", options={"ordering": ["-date"]},
        ),
    ]
