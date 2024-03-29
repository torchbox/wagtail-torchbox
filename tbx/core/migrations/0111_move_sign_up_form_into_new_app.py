# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 22:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0040_page_draft_title"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("wagtailforms", "0003_capitalizeverbose"),
        ("torchbox", "0110_rename_blogpagetaglist_to_tag"),
    ]

    database_operations = [
        migrations.AlterModelTable(
            "SignUpFormPageResponse", "sign_up_form_signupformpageresponse"
        ),
        migrations.AlterModelTable("SignUpFormPage", "sign_up_form_signupformpage"),
        migrations.AlterModelTable(
            "SignUpFormPageBullet", "sign_up_form_signupformpagebullet"
        ),
        migrations.AlterModelTable(
            "SignUpFormPageLogo", "sign_up_form_signupformpagelogo"
        ),
        migrations.AlterModelTable(
            "SignUpFormPageQuote", "sign_up_form_signupformpagequote"
        ),
    ]

    state_operations = [
        migrations.RemoveField(
            model_name="signupformpage", name="call_to_action_image",
        ),
        migrations.RemoveField(model_name="signupformpage", name="email_attachment",),
        migrations.RemoveField(model_name="signupformpage", name="page_ptr",),
        migrations.RemoveField(model_name="signupformpagebullet", name="page",),
        migrations.RemoveField(model_name="signupformpagelogo", name="logo",),
        migrations.RemoveField(model_name="signupformpagelogo", name="page",),
        migrations.RemoveField(model_name="signupformpagequote", name="page",),
        migrations.DeleteModel(name="SignUpFormPageResponse",),
        migrations.DeleteModel(name="SignUpFormPage",),
        migrations.DeleteModel(name="SignUpFormPageBullet",),
        migrations.DeleteModel(name="SignUpFormPageLogo",),
        migrations.DeleteModel(name="SignUpFormPageQuote",),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations, state_operations=state_operations,
        )
    ]
