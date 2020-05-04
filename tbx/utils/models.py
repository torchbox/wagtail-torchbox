from grapple.models import GraphQLCollection, GraphQLForeignKey
from wagtail.core.models import Page
from wagtail_headless_preview.models import HeadlessPreviewMixin


# Base Page
class TorchboxPage(HeadlessPreviewMixin, Page):
    class Meta:
        abstract = True

    def get_prioritised_service(self):
        if hasattr(self, 'related_services'):
            return self.related_services.order_by('sort_order').first()

        return getattr(self, 'service', None)

    @property
    def contact(self):
        from tbx.people.models import Contact

        service = self.get_prioritised_service()
        if service and service.preferred_contact:
            return service.preferred_contact

        return Contact.objects.filter(default_contact=True).first()

    @property
    def preferred_contact_reasons(self):
        from tbx.people.models import ContactReasonsList

        contact_reasons = getattr(self, "contact_reasons", None)
        if contact_reasons:
            return contact_reasons

        contact_reasons = getattr(self.get_prioritised_service(), "contact_reasons", None)
        if contact_reasons:
            return contact_reasons

        return ContactReasonsList.objects.filter(is_default=True).first() or []

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
