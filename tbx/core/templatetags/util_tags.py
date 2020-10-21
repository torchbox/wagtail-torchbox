from django import template
from django.utils.text import camel_case_to_spaces, slugify

register = template.Library()

# Get widget type of a field
@register.filter(name="widget_type")
def widget_type(bound_field):
    return slugify(camel_case_to_spaces(bound_field.field.widget.__class__.__name__))
