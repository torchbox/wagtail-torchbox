from django.test import TestCase

from tbx.taxonomy.factories import ServiceFactory


class ServiceFactoryTestCase(TestCase):
    def test_service_factory(self):
        service = ServiceFactory()
        self.assertIsNotNone(service.name)
        self.assertIsNotNone(service.slug)
        self.assertIsNotNone(service.description)
        self.assertIsNotNone(service.sort_order)
        self.assertIsNotNone(service.preferred_contact)
        self.assertIsNone(service.contact_reasons)

    def test_service_factory_with_contact_reasons(self):
        service = ServiceFactory(contact_reasons=6)
        self.assertIsNotNone(service.name)
        self.assertIsNotNone(service.slug)
        self.assertIsNotNone(service.description)
        self.assertIsNotNone(service.sort_order)
        self.assertIsNotNone(service.preferred_contact)
        self.assertEqual(service.contact_reasons.reasons.count(), 6)
