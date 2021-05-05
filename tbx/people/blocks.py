from django.utils.functional import cached_property

from wagtail.core import blocks
from wagtail.embeds import blocks as embed_blocks, embeds
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
    def embed(self):
        return embeds.get_embed(self.url)


class InstagramEmbedBlock(embed_blocks.EmbedBlock):
    class Meta:
        icon = "fa-instagram"
        template = "patterns/atoms/instagram-post/instagram-post.html"

    def to_python(self, value):
        """Override to replace the EmbedValue with the custom class."""
        if not value:
            return None
        else:
            return InstagramEmbedValue(value)


class InstagramPostGalleryBlock(blocks.StreamBlock):
    posts = blocks.StreamBlock(
        required=False,
        local_blocks=[("post", InstagramEmbedBlock())],
        min_num=8,
        max_num=8,
        template="patterns/molecules/instagram-gallery/instagram-gallery.html",
    )

    class Meta:
        max_num = 1
