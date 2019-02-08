from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.core.signals import page_published, page_unpublished
from django.conf import settings
from .models import Deployment


class NetlifyPermissions(PermissionHelper):
    def user_can_create(self, user):
        return True

    def user_can_list(self, user):
        return True

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_delete_obj(self, user, obj):
        return False


class NetlifyDeploymentAdmin(ModelAdmin):
    model = Deployment
    permission_helper_class = NetlifyPermissions
    menu_label = 'Netlify Deployments'
    menu_icon = 'collapse-up'
    menu_order = 1000
    list_display = ('deployment_created', 'deployment_time', 'deployment_created_by')
    form_fields_exclude = ('deployment_created_by',)


modeladmin_register(NetlifyDeploymentAdmin)


def trigger_deployment(**kwargs):
    if settings.NETLIFY_AUTO_DEPLOY:
        revision = kwargs.get('revision')
        deployment = Deployment(deployment_created_by=revision.user)
        deployment.save()


page_published.connect(trigger_deployment)
page_unpublished.connect(trigger_deployment)
