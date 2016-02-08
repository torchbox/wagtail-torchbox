from django.utils.html import format_html_join, format_html
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import allow_without_attributes

from wagtailmodeladmin.options import ModelAdmin, wagtailmodeladmin_register

from .models import GoogleAdGrantApplication


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'blockquote': allow_without_attributes,
        'span': allow_without_attributes
    }


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'torchbox/js/hallo-plugins/span.js'
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
          registerHalloPlugin('spanbutton');
        </script>
        """
    )


class GoogleAdGrantApplicationModelAdmin(ModelAdmin):
    model = GoogleAdGrantApplication
    menu_label = 'Ad Grant Applications'
    menu_icon = 'date'
    menu_order = 600
    add_to_settings_menu = False
    list_display = ('date', 'name', 'email')

wagtailmodeladmin_register(GoogleAdGrantApplicationModelAdmin)
