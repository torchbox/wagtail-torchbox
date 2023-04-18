from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class StandoutItemsBlock(blocks.StructBlock):
    class LinkBlock(blocks.StreamBlock):
        internal = blocks.PageChooserBlock()
        external = blocks.URLBlock()

        class Meta:
            required = False
            max_num = 1

    subtitle = blocks.CharBlock()
    title = blocks.CharBlock()
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


class InstagramEmbedBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    link = blocks.URLBlock(
        required=False,
        help_text="Link to a specific post here or leave blank for it to link to https://www.instagram.com/torchboxltd/",
    )

    class Meta:
        icon = "group"
