# -*- coding: utf-8 -*-


from django.db import models, migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0005_auto_20150325_1631"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.RichTextField(
                verbose_name="body (deprecated. Use streamfield instead)"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="intro",
            field=wagtail.fields.RichTextField(
                verbose_name="Intro (deprecated. Use streamfield instead)", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="body",
            field=wagtail.fields.RichTextField(
                verbose_name="Body (deprecated. Use streamfield instead)", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="intro",
            field=wagtail.fields.RichTextField(
                verbose_name="Intro (deprecated. Use streamfield instead)", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="workpage",
            name="body",
            field=wagtail.fields.RichTextField(
                verbose_name="Body (deprecated. Use streamfield instead)", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="workpage",
            name="intro",
            field=wagtail.fields.RichTextField(
                verbose_name="Intro (deprecated. Use streamfield instead)", blank=True
            ),
            preserve_default=True,
        ),
    ]
