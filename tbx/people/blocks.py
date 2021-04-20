from wagtail.core import blocks
from wagtail.embeds import blocks as embed_blocks
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


class InstagramPostGalleryBlock(blocks.StreamBlock):
    posts = blocks.StreamBlock(
        required=False,
        local_blocks=[("post", embed_blocks.EmbedBlock())],
        min_num=8,
        max_num=8,
        template="patterns/molecules/instagram-gallery/instagram-gallery.html",
    )

    class Meta:
        max_num = 1
