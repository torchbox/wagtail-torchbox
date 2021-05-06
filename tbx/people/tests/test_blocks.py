from django import test
from django.core import exceptions

from tbx.people.blocks import InstagramEmbedBlock, InstagramEmbedValue


class TestInstagramEmbedBlock(test.TestCase):
    def test_clean_validation_error_non_url(self):
        block = InstagramEmbedBlock()
        value = InstagramEmbedValue("not-a-url")

        with self.assertRaises(exceptions.ValidationError):
            block.clean(value=value)

    def test_clean_validation_error_non_instagram_url(self):
        block = InstagramEmbedBlock()
        value = InstagramEmbedValue("https://example.com")

        with self.assertRaises(exceptions.ValidationError):
            block.clean(value=value)

    def test_clean_validation_error_non_instagram_url_shows_reason(self):
        block = InstagramEmbedBlock()
        value = InstagramEmbedValue("https://example.com")

        with self.assertRaises(exceptions.ValidationError) as cm:
            block.clean(value=value)

        error = cm.exception
        self.assertIn("Instagram", error.message)

    def test_clean_validation_error_instagram_non_post_url(self):
        """This makes sure the override is still using the embed block validation."""
        block = InstagramEmbedBlock()
        value = InstagramEmbedValue("https://www.instagram.com/about")

        with self.assertRaises(exceptions.ValidationError):
            block.clean(value=value)

    def test_clean_returns_value_object_instagram_post_url(self):
        block = InstagramEmbedBlock()
        value = InstagramEmbedValue("https://www.instagram.com/p/COSlPitLfU3/")

        result = block.clean(value=value)

        self.assertEqual(value.url, result.url)
