from tbx.core.models import StandardPage
from tbx.propositions.factories import (
    PropositionPageFactory,
    SubPropositionPageFactory,
)
from tbx.propositions.models import PropositionPage, SubPropositionPage
from wagtail.test.utils import WagtailPageTestCase


class SubPropositionPageTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.proposition_page = PropositionPageFactory()
        cls.sub_proposition_page = SubPropositionPageFactory(
            parent=cls.proposition_page,
        )

    def test_can_create_sub_proposition_page_under_proposition_page(self):
        self.assertCanCreateAt(PropositionPage, SubPropositionPage)

    def test_sub_proposition_page_parent_page_types(self):
        self.assertAllowedParentPageTypes(SubPropositionPage, {PropositionPage})

    def test_sub_proposition_page_subpage_types(self):
        self.assertAllowedSubpageTypes(SubPropositionPage, {StandardPage})

    def test_sub_proposition_page_service(self):
        self.assertEqual(
            self.sub_proposition_page.service, self.proposition_page.service
        )

        another_sub_proposition_page = SubPropositionPageFactory()
        self.assertIsNone(another_sub_proposition_page.service)

    def test_sub_proposition_page_filter_by(self):
        self.assertEqual(
            self.sub_proposition_page.filter_by, self.proposition_page.service.slug
        )

        another_sub_proposition_page = SubPropositionPageFactory()
        self.assertEqual(another_sub_proposition_page.filter_by, "")
