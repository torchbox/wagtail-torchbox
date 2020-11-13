# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0014_workpage_show_in_play_menu"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReasonToJoin",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("body", models.CharField(max_length=511)),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="torchbox.TorchboxImage",
                        null=True,
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="reasons_to_join", to="torchbox.JobIndexPage"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
            bases=(models.Model,),
        ),
        migrations.RemoveField(model_name="jobindexpagecontentblock", name="page",),
        migrations.DeleteModel(name="JobIndexPageContentBlock",),
        migrations.AddField(
            model_name="jobindexpage",
            name="no_jobs_that_fit",
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="jobindexpage",
            name="refer_a_friend",
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="jobindexpage",
            name="terms_and_conditions",
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
