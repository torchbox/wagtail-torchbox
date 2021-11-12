from django.db import migrations


def copy_images(apps, schema_editor):
    # Here we copy and initialise our new image models and their renditions
    CustomImage = apps.get_model("images", "CustomImage")
    Rendition = apps.get_model("images", "Rendition")

    TorchboxImage = apps.get_model("torchbox", "TorchboxImage")
    TorchboxRendition = apps.get_model("torchbox", "TorchboxRendition")

    # Copy old images to new model
    for tbx_image in TorchboxImage.objects.values():
        custom_image = CustomImage.objects.create(**tbx_image)
        custom_image.save()

    # Now we have images, copy the old renditions to new ones
    for tbx_rendition in TorchboxRendition.objects.values():
        rendition = Rendition.objects.create(**tbx_rendition)
        rendition.save()


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        ("torchbox", "0139_homepage_featured_posts_and_hero_image"),
    ]

    operations = [
        # This is a one way migration, TorchboxImage will be removed
        migrations.RunPython(copy_images, migrations.RunPython.noop),
    ]
