from django.db import migrations

def update_dark_transparent_theme(apps, schema_editor):
    page = apps.get_model("propositions", "PropositionPage")
    page.objects.filter(theme='dark--transparent').update(theme='light')

class Migration(migrations.Migration):

    dependencies = [
        ('propositions', '0009_auto_20230503_1527'),
    ]

    operations = [
        migrations.RunPython(update_dark_transparent_theme),
    ]
