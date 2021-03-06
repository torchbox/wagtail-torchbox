# Generated by Django 2.2.17 on 2021-04-09 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0134_remove_googleadgrantspage_and_related_models"),
        ("people", "0020_valuespagevalue"),
    ]

    operations = [
        migrations.AddField(
            model_name="valuespagevalue",
            name="value_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="torchbox.TorchboxImage",
            ),
        ),
    ]
