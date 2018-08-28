from django.core.files.storage import get_storage_class
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers

from storages.backends.s3boto3 import S3Boto3Storage
from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)
from wagtail.core import hooks
from wagtail.documents.models import document_served, get_document_model

from tbx.storages.backends import S3Boto3StorageWithQuerystring

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


@hooks.register('before_serve_document', order=100)
def serve_document_from_s3(document, request):
    # Skip this hook if not using django-storages boto3 backend.
    if not issubclass(get_storage_class(), S3Boto3Storage):
        return

    # Send document_served signal.
    document_served.send(sender=get_document_model(), instance=document,
                         request=request)

    # Get direct S3 link.
    file_url = document.file.url

    # Generate redirect response and add never_cache headers.
    response = redirect(file_url)
    del response['Cache-control']
    add_never_cache_headers(response)
    return response
