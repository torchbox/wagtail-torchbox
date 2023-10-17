from wagtail.snippets.models import register_snippet

from .admin import TaxonomyModelAdminGroup

register_snippet(TaxonomyModelAdminGroup)
