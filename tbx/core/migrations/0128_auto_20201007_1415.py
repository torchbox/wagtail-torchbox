# Generated by Django 2.2.12 on 2020-10-07 13:15

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0127_jobindexpage_intro"),
    ]

    operations = [
        migrations.RenameField(
            model_name="globalsettings",
            old_name="phili_address_link",
            new_name="us_address_link",
        ),
        migrations.RenameField(
            model_name="globalsettings",
            old_name="phili_address_svg",
            new_name="us_address_svg",
        ),
        migrations.RenameField(
            model_name="globalsettings",
            old_name="phili_address",
            new_name="us_address_title",
        ),
        migrations.RemoveField(
            model_name="globalsettings", name="phili_address_title",
        ),
        migrations.AddField(
            model_name="globalsettings",
            name="us_address",
            field=wagtail.fields.RichTextField(default="", help_text="Full address"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalsettings",
            name="bristol_address",
            field=wagtail.fields.RichTextField(help_text="Full address"),
        ),
        migrations.AlterField(
            model_name="globalsettings",
            name="oxford_address",
            field=wagtail.fields.RichTextField(help_text="Full address"),
        ),
    ]
