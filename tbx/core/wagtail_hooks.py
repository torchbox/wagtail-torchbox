from django.utils.html import format_html_join, format_html
from django.conf import settings

from wagtail.core import hooks

from wagtail.contrib.modeladmin.options import ModelAdminGroup, ModelAdmin, modeladmin_register

from .models import GoogleAdGrantApplication, SignUpFormPageResponse

from wagtail.admin.rich_text import HalloPlugin


@hooks.register('register_rich_text_features')
def register_embed_feature(features):
    features.register_editor_plugin(
        'hallo', 'span',
        HalloPlugin(
            name='spanbutton',
            js=['torchbox/js/hallo-plugins/span.js'],
        )
    )


class GoogleAdGrantApplicationModelAdmin(ModelAdmin):
    model = GoogleAdGrantApplication
    menu_label = 'Ad Grant Applications'
    menu_icon = 'date'
    menu_order = 600
    add_to_settings_menu = False
    list_display = ('date', 'name', 'email')


class SignUpFormPageResponseModelAdmin(ModelAdmin):
    model = SignUpFormPageResponse
    menu_label = 'Sign-Up Form Page Submissions'
    menu_icon = 'date'
    menu_order = 600
    add_to_settings_menu = False
    list_display = ('date', 'email')


class SubmissionsModelAdminGroup(ModelAdminGroup):
    menu_label = 'Form Submissions'
    menu_icon = 'folder-open-inverse' # change as required
    menu_order = 600
    items = (SignUpFormPageResponseModelAdmin, GoogleAdGrantApplicationModelAdmin)

modeladmin_register(SubmissionsModelAdminGroup)


@hooks.register('insert_global_admin_css')
def import_fontawesome_stylesheet():
    elem = '<link rel="stylesheet" href="{}torchbox/vendor/fontawesome/css/font-awesome.min.css">'.format(
        settings.STATIC_URL
    )
    return format_html(elem)
