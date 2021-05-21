from django.core import exceptions
from django.template import loader as template_loader
from django.utils import functional as utils_functional

from wagtail.core import blocks
from wagtail.embeds import blocks as embed_blocks
from wagtail.embeds import embeds
from wagtail.embeds import exceptions as embed_exceptions
from wagtail.images.blocks import ImageChooserBlock


class StandoutItemsBlock(blocks.StructBlock):
    class LinkBlock(blocks.StreamBlock):
        internal = blocks.PageChooserBlock()
        external = blocks.URLBlock()

        class Meta:
            required = False
            max_num = 1

    title = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    description = blocks.TextBlock()
    image = ImageChooserBlock()
    link = LinkBlock()

    class Meta:
        icon = "pick"

    @staticmethod
    def get_link(value):
        """The link could be internal or external."""
        try:
            link = value[0]
        except IndexError:
            return ""
        else:
            return (
                link.value.url
                if link.block_type == "internal" and link.value
                else link.value
            )


class InstagramEmbedValue(embed_blocks.EmbedValue):
    """Custom Embed value that allow access to represented embed object."""

    @utils_functional.cached_property
    def html(self):
        try:
            embed = embeds.get_embed(self.url)
        except embed_exceptions.EmbedException:
            return ""

        return template_loader.render_to_string(
            template_name="patterns/atoms/instagram-post/instagram-post.html",
            context={"embed": embed,},
        )


class InstagramEmbedBlock(embed_blocks.EmbedBlock):
    class Meta:
        icon = "fa-instagram"

    def value_from_form(self, value):
        """Override to replace the EmbedValue with the custom class."""
        if not value:
            return None
        else:
            return InstagramEmbedValue(value)

    def to_python(self, value):
        """
        Override to replace the EmbedValue with the custom class.

        This makes use of the fact that in the original EmbedBlock, the
        `value_from_form` and `to_python` functions are identical.

        """
        return self.value_from_form(value)

    def clean(self, value):
        if isinstance(value, InstagramEmbedValue) and not value.url.startswith(
            "https://www.instagram.com/"
        ):
            raise exceptions.ValidationError("Please specify an Instagram URL.")
        return super().clean(value)


class InstagramPostGalleryBlock(blocks.StreamBlock):
    posts = blocks.StreamBlock(
        required=False,
        local_blocks=[("post", InstagramEmbedBlock())],
        min_num=8,
        max_num=8,
        template="patterns/molecules/instagram-gallery/instagram-gallery.html",
        icon="fa-instagram",
    )

    class Meta:
        max_num = 1
