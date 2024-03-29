# Generated by Django 2.2.13 on 2020-11-17 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0029_subservice_listingsettings"),
        ("wagtailforms", "0004_add_verbose_name_plural"),
        ("wagtailredirects", "0006_redirect_increase_max_length"),
        ("people", "0017_update_streamblock_templates"),
        ("wagtailcore", "0052_pagelogentry"),
        ("torchbox", "0134_remove_googleadgrantspage_and_related_models"),
        ("sign_up_form", "0001_initial"),
    ]

    operations = [
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
