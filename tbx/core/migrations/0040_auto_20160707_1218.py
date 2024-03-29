# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-07 11:18


from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("torchbox", "0039_auto_20160706_1716"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactFormField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "label",
                    models.CharField(
                        help_text="The label of the form field",
                        max_length=255,
                        verbose_name="label",
                    ),
                ),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("singleline", "Single line text"),
                            ("multiline", "Multi-line text"),
                            ("email", "Email"),
                            ("number", "Number"),
                            ("url", "URL"),
                            ("checkbox", "Checkbox"),
                            ("checkboxes", "Checkboxes"),
                            ("dropdown", "Drop down"),
                            ("radio", "Radio buttons"),
                            ("date", "Date"),
                            ("datetime", "Date/time"),
                        ],
                        max_length=16,
                        verbose_name="field type",
                    ),
                ),
                (
                    "required",
                    models.BooleanField(default=True, verbose_name="required"),
                ),
                (
                    "choices",
                    models.CharField(
                        blank=True,
                        help_text="Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.",
                        max_length=512,
                        verbose_name="choices",
                    ),
                ),
                (
                    "default_value",
                    models.CharField(
                        blank=True,
                        help_text="Default value. Comma separated values supported for checkboxes.",
                        max_length=255,
                        verbose_name="default value",
                    ),
                ),
                (
                    "help_text",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="help text"
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
        migrations.AlterModelOptions(
            name="contact", options={"verbose_name": "Contact Page"},
        ),
        migrations.AddField(
            model_name="contact",
            name="from_address",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="from address"
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="subject",
            field=models.CharField(blank=True, max_length=255, verbose_name="subject"),
        ),
        migrations.AddField(
            model_name="contact",
            name="thank_you_text",
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="to_address",
            field=models.CharField(
                blank=True,
                help_text="Optional - form submissions will be emailed to this address",
                max_length=255,
                verbose_name="to address",
            ),
        ),
        migrations.AlterField(
            model_name="contact",
            name="intro",
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name="contactformfield",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contact_form_fields",
                to="torchbox.Contact",
            ),
        ),
    ]
