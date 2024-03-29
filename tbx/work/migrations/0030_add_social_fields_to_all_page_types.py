# Generated by Django 3.2.18 on 2023-08-02 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_wagtail42_images'),
        ('work', '0029_add_mailchimp_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='workindexpage',
            name='social_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage'),
        ),
        migrations.AddField(
            model_name='workindexpage',
            name='social_text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='workpage',
            name='social_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage'),
        ),
        migrations.AddField(
            model_name='workpage',
            name='social_text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
