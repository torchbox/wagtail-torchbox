from django.test import TestCase

from tbx.propositions.factories import (
    PropositionPageFactory,
    SubPropositionPageFactory,
)


class PropositionPageFactoryTestCase(TestCase):
    def test_proposition_page_factory(self):
        proposition_page = PropositionPageFactory()
        self.assertIsNotNone(proposition_page.title)
        self.assertIsNotNone(proposition_page.strapline)
        self.assertIsNotNone(proposition_page.service)


class SubPropositionPageFactoryTestCase(TestCase):
    def test_sub_proposition_page_factory(self):
        sub_proposition_page = SubPropositionPageFactory()
        self.assertIsNotNone(sub_proposition_page.title)
        self.assertIsNotNone(sub_proposition_page.strapline)
