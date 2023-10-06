from django.contrib.admin.utils import quote
from django.core.exceptions import PermissionDenied
from django.urls import re_path
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from wagtail_modeladmin.helpers import ButtonHelper
from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup
from wagtail_modeladmin.views import DeleteView, InstanceSpecificView

from . import models


class ServiceModelAdmin(SnippetViewSet):
    model = models.Service
    base_url_path = "taxonomy/service"
    list_display = ("name", "slug", "sort_order")
    ordering = ["sort_order"]


class TaxonomyModelAdminGroup(SnippetViewSetGroup):
    menu_label = "Taxonomy"
    menu_icon = "folder-open-inverse"
    menu_order = 750
    items = [ServiceModelAdmin]
