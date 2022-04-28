from django.core.files.storage import get_storage_class
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers

from storages.backends.s3boto3 import S3Boto3Storage
from wagtail import hooks
from wagtail.documents import get_document_model
from wagtail.documents.models import document_served


@hooks.register("before_serve_document", order=100)
def serve_document_from_s3(document, request):
    # Skip this hook if not using django-storages boto3 backend.
    if not issubclass(get_storage_class(), S3Boto3Storage):
        return

    # Send document_served signal.
    document_served.send(
        sender=get_document_model(), instance=document, request=request
    )

    # Get direct S3 link.
    file_url = document.file.url

    # Generate redirect response and add never_cache headers.
    response = redirect(file_url)
    del response["Cache-control"]
    add_never_cache_headers(response)
    return response


@hooks.register("construct_settings_menu")
def hide_main_menu_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "main-menu"]
