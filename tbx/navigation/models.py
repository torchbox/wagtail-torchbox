from modelcluster.models import ClusterableModel
from wagtail.admin.panels import StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail import blocks
from wagtail.fields import StreamField


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


class CardLinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title", required=False
    )
    description = blocks.CharBlock(
        help_text="Optional text to appear under the title", required=False
    )

    class Meta:
        template = ("patterns/molecules/navigation/blocks/teaser.html",)


@register_setting(icon="list-ul")
class NavigationSettings(BaseSetting, ClusterableModel):
    primary_navigation = StreamField(
        [("link", LinkBlock())], 
        blank=True, 
        help_text="Main site navigation",
        use_json_field=True
    )
    footer_links = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Single list of elements at the base of the page.",
        use_json_field=True
    )
    footer_teasers = StreamField(
        [("link", CardLinkBlock())],
        blank=True,
        help_text="Row of links that use prominent styles to standout.",
        use_json_field=True
    )
    footer_top_links = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Single list of links that appear between the teasers and the addresses.",
        use_json_field=True
    )

    panels = [
        StreamFieldPanel("primary_navigation"),
        StreamFieldPanel("footer_teasers"),
        StreamFieldPanel("footer_top_links"),
        StreamFieldPanel("footer_links"),
    ]
