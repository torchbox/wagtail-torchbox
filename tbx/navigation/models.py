from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from modelcluster.models import ClusterableModel
from tbx.core.blocks import ImageWithLinkBlock
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField


class LinkBlockStructValue(blocks.StructValue):
    def url(self):
        if page := self.get("page"):
            return page.url

        if external_link := self.get("external_link"):
            return external_link

        return ""

    def text(self):
        if self.get("page") and not self.get("title"):
            return self.get("page").title
        return self.get("title")

    def is_page(self):
        return bool(self.get("page"))


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title", required=False
    )

    class Meta:
        value_class = LinkBlockStructValue

    def clean(self, value):
        struct_value = super().clean(value)

        errors = {}
        page = value.get("page")
        external_link = value.get("external_link")

        if not page and not external_link:
            error = ErrorList(
                [ValidationError("You must specify either a page or an external link")]
            )
            errors["page"] = errors["external_link"] = error

        if page and external_link:
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify either a page or an external link, not both"
                    )
                ]
            )
            errors["external_link"] = errors["page"] = error

        if not value.get("title") and external_link:
            error = ErrorList(
                [ValidationError("You must specify the link title for external links")]
            )
            errors["title"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value


@register_setting(icon="list-ul")
class NavigationSettings(BaseSiteSetting, ClusterableModel):
    primary_navigation = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Main site navigation",
        use_json_field=True,
    )
    footer_links = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Single list of elements at the base of the page.",
        use_json_field=True,
    )
    footer_logos = StreamField(
        [("logos", ImageWithLinkBlock())],
        blank=True,
        help_text="Single list of logos that appear before the footer box",
        use_json_field=True,
        max_num=4,
    )

    panels = [
        FieldPanel("primary_navigation"),
        FieldPanel("footer_links"),
        FieldPanel("footer_logos"),
    ]
