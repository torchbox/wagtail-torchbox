# Generated by Django 2.2.13 on 2020-11-17 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0052_pagelogentry"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("services", "0029_subservice_listingsettings"),
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("people", "0017_update_streamblock_templates"),
        ("torchbox", "0132_update_streamblock_templates"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aboutpagecontentblock",
            name="image",
        ),
        migrations.RemoveField(
            model_name="aboutpagecontentblock",
            name="page",
        ),
        migrations.RemoveField(
            model_name="aboutpageoffice",
            name="page",
        ),
        migrations.RemoveField(
            model_name="aboutpagerelatedlinkbutton",
            name="link_document",
        ),
        migrations.RemoveField(
            model_name="aboutpagerelatedlinkbutton",
            name="link_page",
        ),
        migrations.RemoveField(
            model_name="aboutpagerelatedlinkbutton",
            name="page",
        ),
        migrations.DeleteModel(
            name="AboutPage",
        ),
        migrations.DeleteModel(
            name="AboutPageContentBlock",
        ),
        migrations.DeleteModel(
            name="AboutPageOffice",
        ),
        migrations.DeleteModel(
            name="AboutPageRelatedLinkButton",
        ),
    ]
