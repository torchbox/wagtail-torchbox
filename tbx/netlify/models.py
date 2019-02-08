import time
import requests
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.db import models
from django.conf import settings
from django.utils import timezone


@register_setting
class NetlifySettings(BaseSetting):
    netlify_url = models.URLField(help_text='URL of Netlify Site')
    netlify_build_trigger = models.URLField(help_text='Netlify unique build trigger URL')


class Deployment(models.Model):
    deployment_created = models.DateTimeField(
        editable=False
    )
    deployment_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Trigger deployment at this time (Leave blank to deploy now)'
    )
    deployment_created_by = models.TextField(
        blank=True,
        default=''
    )

    def save(self, *args, **kwargs):
        if self.deployment_created is None:
            self.deployment_created_by = 'Admin'

        self.deployment_created = timezone.now()
        if self.deployment_time is None:
            self.deployment_time = self.deployment_created

        deploy()
        super(Deployment, self).save(*args, **kwargs)


def deploy():
    req = requests.post(settings.NETLIFY_TRIGGER_URL)
