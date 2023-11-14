# Generated by Django 3.2.18 on 2023-06-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0039_data_migration_service_theme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicepage",
            name="theme",
            field=models.CharField(
                choices=[("light", "Light"), ("coral", "Coral"), ("dark", "Dark")],
                default="light",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="subservicepage",
            name="theme",
            field=models.CharField(
                choices=[("light", "Light"), ("coral", "Coral"), ("dark", "Dark")],
                default="light",
                max_length=255,
            ),
        ),
    ]
