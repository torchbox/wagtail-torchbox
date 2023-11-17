from django.db import migrations

def update_theme(apps, schema_editor):
    page = apps.get_model('services', 'SubServicePage')
    page.objects.filter(theme='dark--transparent').update(theme='light')

class Migration(migrations.Migration):

    dependencies = [
        ('services', '0037_alter_subservicepage_content'),
    ]

    operations = [
        migrations.RunPython(update_theme),
    ]
