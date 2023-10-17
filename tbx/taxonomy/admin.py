from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from . import models


class TaxonomyModelAdmin(SnippetViewSet):
    def get_admin_urls_for_registration(self):
        return super().get_admin_urls_for_registration()


class ServiceModelAdmin(TaxonomyModelAdmin):
    model = models.Service
    base_url_path = "taxonomy/service"
    list_display = ("name", "slug", "sort_order")
    ordering = ["sort_order"]


class TaxonomyModelAdminGroup(SnippetViewSetGroup):
    menu_label = "Taxonomy"
    menu_icon = "folder-open-inverse"
    menu_order = 750
    items = [ServiceModelAdmin]
