from wagtail.contrib.modeladmin.options import modeladmin_register

from .admin import TaxonomyModelAdminGroup

modeladmin_register(TaxonomyModelAdminGroup)
