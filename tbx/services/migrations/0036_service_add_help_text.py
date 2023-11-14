# Generated by Django 3.2.16 on 2023-03-20 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0035_services_processes_section_embed_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicepage",
            name="case_studies_section_title",
            field=models.TextField(
                blank=True,
                default="Work",
                help_text="Leave this field empty to hide the case studies section.",
            ),
        ),
        migrations.AlterField(
            model_name="servicepage",
            name="testimonials_section_title",
            field=models.TextField(
                blank=True,
                default="Clients",
                help_text="Leave this field empty to hide the testimonials section.",
            ),
        ),
        migrations.AlterField(
            model_name="subservicepage",
            name="case_studies_section_title",
            field=models.TextField(
                blank=True,
                default="Work",
                help_text="Leave this field empty to hide the case studies section.",
            ),
        ),
        migrations.AlterField(
            model_name="subservicepage",
            name="testimonials_section_title",
            field=models.TextField(
                blank=True,
                default="Clients",
                help_text="Leave this field empty to hide the testimonials section.",
            ),
        ),
    ]
