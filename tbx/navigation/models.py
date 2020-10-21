from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import StreamField


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title", required=False
    )

    class Meta:
        template = ("patterns/molecules/navigation/blocks/menu_item.html",)


class LinkColumnWithHeader(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False, help_text="Leave blank if no header required."
    )
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        template = ("patterns/molecules/navigation/blocks/footer_column.html",)


@register_setting(icon="list-ul")
class NavigationSettings(BaseSetting, ClusterableModel):
    primary_navigation = StreamField(
        [("link", LinkBlock())], blank=True, help_text="Main site navigation"
    )
    secondary_navigation = StreamField(
        [("link", LinkBlock())], blank=True, help_text="Alternative navigation"
    )
    footer_navigation = StreamField(
        [("column", LinkColumnWithHeader())],
        blank=True,
        help_text="Multiple columns of footer links with optional header.",
    )
    footer_links = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Single list of elements at the base of the page.",
    )

    panels = [
        StreamFieldPanel("primary_navigation"),
        StreamFieldPanel("secondary_navigation"),
        StreamFieldPanel("footer_navigation"),
        StreamFieldPanel("footer_links"),
    ]
