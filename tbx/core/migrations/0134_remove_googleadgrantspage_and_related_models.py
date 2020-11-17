# Generated by Django 2.2.13 on 2020-11-17 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailsearchpromotions", "0002_capitalizeverbose"),
        ("people", "0017_update_streamblock_templates"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("wagtailcore", "0052_pagelogentry"),
        ("services", "0029_subservice_listingsettings"),
        ("torchbox", "0133_remove_aboutpage_and_related_models"),
    ]

    operations = [
        migrations.DeleteModel(name="GoogleAdGrantApplication",),
        migrations.RemoveField(model_name="googleadgrantspage", name="page_ptr",),
        migrations.RemoveField(
            model_name="googleadgrantspagegrantsmanaged", name="image",
        ),
        migrations.RemoveField(
            model_name="googleadgrantspagegrantsmanaged", name="page",
        ),
        migrations.RemoveField(model_name="googleadgrantspagequote", name="page",),
        migrations.DeleteModel(name="GoogleAdGrantsAccreditations",),
        migrations.DeleteModel(name="GoogleAdGrantsPage",),
        migrations.DeleteModel(name="GoogleAdGrantsPageGrantsManaged",),
        migrations.DeleteModel(name="GoogleAdGrantsPageQuote",),
    ]
