from django.conf import settings
from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)
from wagtail.core import hooks

from .models import GoogleAdGrantApplication, SignUpFormPageResponse


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
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 600
    items = (SignUpFormPageResponseModelAdmin, GoogleAdGrantApplicationModelAdmin)


modeladmin_register(SubmissionsModelAdminGroup)
