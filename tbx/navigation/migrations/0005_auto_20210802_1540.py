# Generated by Django 2.2.17 on 2021-08-02 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("navigation", "0004_navigationsettings_footer_top_links"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="navigationsettings", name="footer_navigation",
        ),
        migrations.RemoveField(
            model_name="navigationsettings", name="secondary_navigation",
        ),
    ]
