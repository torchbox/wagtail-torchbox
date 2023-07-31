# Generated by Django 3.2.18 on 2023-08-02 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_wagtail42_images'),
        ('propositions', '0010_merge_20230620_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='propositionpage',
            name='social_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage'),
        ),
        migrations.AddField(
            model_name='propositionpage',
            name='social_text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]