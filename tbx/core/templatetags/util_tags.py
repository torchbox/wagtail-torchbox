from django import template
from django.utils.text import camel_case_to_spaces, slugify

from tbx.core.utils.models import SocialMediaSettings

register = template.Library()


# Social text
@register.filter(name="social_text")
def social_text(page, site):
    try:
        return page.social_text
    except AttributeError:
        return SocialMediaSettings.for_site(site).default_sharing_text


# Get widget type of a field
@register.filter(name="widget_type")
def widget_type(bound_field):
    return slugify(camel_case_to_spaces(bound_field.field.widget.__class__.__name__))


@register.simple_tag(takes_context=True)
def social_media_settings(context):
    return SocialMediaSettings.for_request(request=context["request"])
