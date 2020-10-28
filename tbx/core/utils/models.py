from django.db import models

from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel

SEARCH_DESCRIPTION_LABEL = "Meta description"  # NOTE changing this requires migrations


# Generic social fields abstract class to add social image/text to any new content type easily.
class SocialFields(models.Model):
    social_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    social_text = models.CharField(max_length=255, blank=True)


    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel(
            [ImageChooserPanel("social_image"), FieldPanel("social_text")],
            "Social networks",
        )
    ]


@register_setting
class SocialMediaSettings(BaseSetting):
    twitter_handle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your Twitter username without the @, e.g. katyperry",
    )
    facebook_app_id = models.CharField(
        max_length=255, blank=True, help_text="Your Facebook app ID."
    )
    default_sharing_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Default sharing text to use if social text has not been set on a page.",
    )
    site_name = models.CharField(
        max_length=255,
        blank=True,
        default="{{ cookiecutter.project_name }}",
        help_text="Site name, used by Open Graph.",
    )
