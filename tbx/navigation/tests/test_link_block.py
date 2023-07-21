from django.core.exceptions import ValidationError
from django.test import TestCase

import wagtail_factories
from tbx.core.models import HomePage
from tbx.images.models import CustomImage
from tbx.navigation.models import LinkBlock, LinkBlockStructValue


class CustomImageFactory(wagtail_factories.ImageFactory):
    credit = "Custom Image credit"

    class Meta:
        model = CustomImage


class HomePageFactory(wagtail_factories.PageFactory):
    title = "Home"

    class Meta:
        model = HomePage


class TestLinkBlock(TestCase):
    def setUp(self):
        root_page = wagtail_factories.PageFactory(parent=None)
        self.home_page = HomePageFactory(parent=root_page)

    def test_link_block_definition(self):
        link_block = LinkBlock()
        self.assertEqual(
            list(link_block.child_blocks.keys()), ["page", "external_link", "title"]
        )
        default_value = link_block.get_default()
        self.assertIsInstance(default_value, LinkBlockStructValue)

    def test_link_block_with_page_no_title_override(self):
        link_block = LinkBlock()
        block_definition = {
            "page": self.home_page.pk,
            "external_link": "",
            "title": "",
        }
        struct_value = link_block.to_python(block_definition)
        self.assertTrue(struct_value.is_page())
        self.assertEqual(struct_value.text(), self.home_page.title)
        self.assertEqual(struct_value.url(), self.home_page.url)

    def test_link_block_with_page_and_title_override(self):
        link_block = LinkBlock()
        block_definition = {
            "page": self.home_page.pk,
            "external_link": "",
            "title": "Custom Title",
        }
        struct_value = link_block.to_python(block_definition)
        self.assertTrue(struct_value.is_page())
        self.assertEqual(struct_value.text(), block_definition.get("title"))
        self.assertEqual(struct_value.url(), self.home_page.url)

    def test_link_block_with_external_link(self):
        link_block = LinkBlock()
        block_definition = {
            "page": None,
            "external_link": "https://www.example.com",
            "title": "An external link",
        }
        struct_value = link_block.to_python(block_definition)
        self.assertFalse(struct_value.is_page())
        self.assertEqual(struct_value.text(), block_definition.get("title"))
        self.assertEqual(struct_value.url(), block_definition.get("external_link"))


class TestLinkBlockValidation(TestCase):
    def setUp(self):
        root_page = wagtail_factories.PageFactory(parent=None)
        self.home_page = HomePageFactory(parent=root_page)

    def test_link_block_with_no_external_link_and_no_page(self):
        link_block = LinkBlock()
        invalid_data = {
            "page": None,
            "external_link": "",
            "title": "An external link",
        }

        with self.assertRaises(ValidationError):
            link_block.clean(invalid_data)

    def test_link_block_with_page_and_external_link(self):
        link_block = LinkBlock()
        invalid_data = {
            "page": self.home_page.pk,
            "external_link": "https://www.example.com",
            "title": "An external link",
        }

        with self.assertRaises(ValidationError):
            link_block.clean(invalid_data)

    def test_link_block_with_external_link_no_title(self):
        link_block = LinkBlock()
        invalid_data = {
            "page": None,
            "external_link": "https://www.example.com",
            "title": "",
        }

        with self.assertRaises(ValidationError):
            link_block.clean(invalid_data)
