# Generated by Django 2.1.5 on 2019-02-07 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0009_auto_20190206_2323"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicepage",
            name="blogs_section_title",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="servicepage",
            name="case_studies_section_title",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="servicepage",
            name="key_points_section_title",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="servicepage",
            name="testimonials_section_title",
            field=models.TextField(blank=True),
        ),
    ]
