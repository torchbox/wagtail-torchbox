from django.db import models

from wagtail.core.models import Page
from wagtail_headless_preview.models import HeadlessPreviewMixin
from grapple.models import GraphQLString, GraphQLForeignKey, GraphQLCollection


# Base Page
class TorchboxPage(HeadlessPreviewMixin, Page):
    class Meta:
        abstract = True

    def get_prioritised_service(self):
        if hasattr(self, 'related_services'):
            return self.related_services.order_by('sort_order').first()

        if hasattr(self, 'service'):
            return self.service

        return None

    @property
    def contact(self):
        from tbx.people.models import Contact

        service = self.get_prioritised_service()
        if service is not None:
            if service.preferred_contact is not None:
                return service.preferred_contact
        try:
            return Contact.objects.get(default_contact=True)
        except Contact.DoesNotExist:
            return None

    @property
    def preferred_contact_reasons(self):
        from tbx.people.models import ContactReasonsList

        if hasattr(self, 'contact_reasons'):
            if self.contact_reasons is not None:
                return self.contact_reasons

        service = self.get_prioritised_service()
        if service is not None:
            if service.contact_reasons is not None:
                return service.contact_reasons

        try:
            return ContactReasonsList.objects.get(is_default=True)
        except ContactReasonsList.DoesNotExist:
            return []

    @property
    def page_related_services(self):
        if hasattr(self, 'related_services'):
            return self.related_services.order_by('sort_order').all()

        return []

    graphql_fields = [
        GraphQLForeignKey(
            'contact',
            'people.Contact'
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            'related_services',
            'taxonomy.Service',
            source='page_related_services'
        ),
        GraphQLForeignKey('contact_reasons', 'people.ContactReasonsList', source='preferred_contact_reasons')
    ]
