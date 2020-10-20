# Generated by Django 2.1.5 on 2019-03-22 00:00

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('torchbox', '0125_auto_20190216_1713'),
        ('work', '0018_workpage_client'),
        ('people', '0014_contactreasonslist_is_default_not_unique'),
        ('blog', '0019_blogpage_body_word_count'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('services', '0026_delete_subservice_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubServicePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('theme', models.CharField(choices=[('light', 'Light'), ('coral', 'Coral'), ('dark', 'Dark'), ('dark--transparent', 'Dark with transparent header')], default='light', max_length=255)),
                ('strapline', models.CharField(max_length=255)),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('greeting_image_type', models.CharField(blank=True, choices=[('woman-left', 'Woman (Left Aligned)'), ('man-left', 'Man (Left aligned)'), ('wagtail', 'Wagtail (Right aligned)')], default='woman-left', max_length=255, null=True)),
                ('heading_for_key_points', wagtail.core.fields.RichTextField(blank=True)),
                ('use_process_block_image', models.BooleanField(default=False)),
                ('heading_for_processes', models.TextField(blank=True, null=True)),
                ('key_points_section_title', models.TextField(blank=True, default='Services')),
                ('testimonials_section_title', models.TextField(blank=True, default='Clients')),
                ('case_studies_section_title', models.TextField(blank=True, default='Work')),
                ('blogs_section_title', models.TextField(blank=True, default='Thinking')),
                ('process_section_title', models.TextField(blank=True, default='Process')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='people.Contact')),
                ('contact_reasons', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='people.ContactReasonsList')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='SubServicePageClientLogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torchbox.TorchboxImage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_logos', to='services.SubServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubServicePageFeaturedBlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_blog_posts', to='services.SubServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubServicePageFeaturedCaseStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('case_study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.WorkPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_case_studies', to='services.SubServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubServicePageKeyPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('text', models.CharField(max_length=255)),
                ('linked_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_points', to='services.SubServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubServicePageProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('page_link_label', models.TextField(blank=True, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='processes', to='services.SubServicePage')),
                ('page_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubServicePageTestimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('quote', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='services.SubServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubServicePageUSAClientLogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torchbox.TorchboxImage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='usa_client_logos', to='services.SubServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='servicepageclientlogo',
            options={},
        ),
        migrations.AlterModelOptions(
            name='servicepagefeaturedblogpost',
            options={},
        ),
        migrations.AlterModelOptions(
            name='servicepagefeaturedcasestudy',
            options={},
        ),
        migrations.AlterModelOptions(
            name='servicepagekeypoint',
            options={},
        ),
        migrations.AlterModelOptions(
            name='servicepageprocess',
            options={},
        ),
        migrations.AlterModelOptions(
            name='servicepagetestimonial',
            options={},
        ),
        migrations.AlterModelOptions(
            name='servicepageusaclientlogo',
            options={},
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='heading_for_key_points',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
