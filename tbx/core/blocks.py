from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.functional import cached_property

from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    FieldBlock,
    ListBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    StructValue,
    URLBlock,
)
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail_webstories.blocks import (
    ExternalStoryEmbedBlock as WebstoryExternalStoryEmbedBlock,
)
from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmedia.blocks import VideoChooserBlock


class LinkStructValue(StructValue):
    @cached_property
    def url(self):
        if page := self.get("page"):
            return page.get_url()
        elif link_url := self.get("link_url"):
            return link_url

    @cached_property
    def text(self):
        if link_text := self.get("link_text"):
            return link_text
        elif page := self.get("page"):
            return page.title


class InternalLinkBlock(StructBlock):
    page = PageChooserBlock()
    link_text = CharBlock(required=False)

    class Meta:
        label = "Internal link"
        icon = "link"
        value_class = LinkStructValue


class ExternalLinkBlock(StructBlock):
    link_url = URLBlock(label="URL")
    link_text = CharBlock()

    class Meta:
        label = "External link"
        icon = "link"
        value_class = LinkStructValue


class LinkBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()

    class Meta:
        label = "Link"
        icon = "link"
        max_num = 1


class KeyPoint(StructBlock):
    title = CharBlock()
    intro = CharBlock()
    link = PageChooserBlock()

    class Meta:
        icon = "form"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(
        choices=(
            ("left", "Wrap left"),
            ("right", "Wrap right"),
            ("half", "Half width"),
            ("full", "Full width"),
        )
    )


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alignment = ImageFormatChoiceBlock()
    caption = CharBlock()
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"


class ImageWithLinkBlock(StructBlock):
    image = ImageChooserBlock()
    link = LinkBlock(required=False)

    class Meta:
        icon = "site"


class PhotoGridBlock(StructBlock):
    images = ListBlock(ImageChooserBlock())

    class Meta:
        icon = "grip"


class PullQuoteBlock(StructBlock):
    quote = CharBlock(form_classname="quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class PullQuoteImageBlock(StructBlock):
    quote = CharBlock()
    attribution = CharBlock()
    image = ImageChooserBlock(required=False)


class TestimonialBlock(StructBlock):
    quote = CharBlock(form_classname="quote title")
    name = CharBlock()
    role = CharBlock()
    link = LinkBlock(required=False)

    class Meta:
        icon = "openquote"


class BustoutBlock(StructBlock):
    image = ImageChooserBlock()
    text = RichTextBlock()

    class Meta:
        icon = "pick"


class WideImage(StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"


class StatsBlock(StructBlock):
    pass

    class Meta:
        icon = "order"


class ExternalStoryEmbedBlock(WebstoryExternalStoryEmbedBlock):
    # Work around due to Attribute Error https://github.com/torchbox/wagtail-webstories/pull/12
    def get_prep_value(self, value):
        if value is None:
            return ""
        elif isinstance(value, str):
            return value
        else:
            return value.url


class EmbedPlusCTABlock(StructBlock):
    title = CharBlock()
    intro = CharBlock()
    link = PageChooserBlock(required=False)
    external_link = URLBlock(label="External Link", required=False)
    button_text = CharBlock()
    image = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False, label="Youtube Embed")

    def clean(self, value):
        struct_value = super().clean(value)

        errors = {}
        image = value.get("image")
        embed = value.get("embed")

        if image and embed:
            error = ErrorList(
                [
                    ValidationError(
                        "Either an image or a Youtube embed may be specified, but not both."
                    )
                ]
            )
            errors["image"] = errors["embed"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value


class CTABlock(StructBlock):
    text = CharBlock(
        help_text="Words in  &lt;span&gt; tag will display in a contrasting colour."
    )
    link = LinkBlock()


class VideoBlock(StructBlock):
    video = VideoChooserBlock()
    # setting autoplay to True adds 'autoplay', 'loop' & 'muted' attrs to video element
    autoplay = BooleanBlock(
        required=False,
        default=False,
        help_text="Automatically start and loop the video. Please use sparingly.",
    )
    use_original_width = BooleanBlock(
        required=False,
        default=False,
        help_text="Use the original width of the video instead of the default content width. "
        "Note that videos wider than the content width will be limited to the content width.",
    )

    class Meta:
        icon = "media"
        template = "patterns/molecules/streamfield/blocks/video_block.html"


class StoryBlock(StreamBlock):
    h2 = CharBlock(
        form_classname="title",
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading2_block.html",
    )
    h3 = CharBlock(
        form_classname="title",
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading3_block.html",
    )
    h4 = CharBlock(
        form_classname="title",
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading4_block.html",
    )
    intro = RichTextBlock(
        icon="pilcrow",
        template="patterns/molecules/streamfield/blocks/intro_block.html",
    )
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="patterns/molecules/streamfield/blocks/paragraph_block.html",
    )
    aligned_image = ImageBlock(
        label="Aligned image",
        template="patterns/molecules/streamfield/blocks/aligned_image_block.html",
    )
    wide_image = WideImage(
        label="Wide image",
        template="patterns/molecules/streamfield/blocks/wide_image_block.html",
    )
    bustout = BustoutBlock(
        template="patterns/molecules/streamfield/blocks/bustout_block.html"
    )
    pullquote = PullQuoteBlock(
        template="patterns/molecules/streamfield/blocks/pullquote_block.html"
    )
    raw_html = RawHTMLBlock(
        label="Raw HTML",
        icon="code",
        template="patterns/molecules/streamfield/blocks/raw_html_block.html",
    )
    mailchimp_form = RawHTMLBlock(
        label="Mailchimp embedded form",
        icon="code",
        template="patterns/molecules/streamfield/blocks/mailchimp_form_block.html",
    )
    markdown = MarkdownBlock(
        icon="code",
        template="patterns/molecules/streamfield/blocks/markdown_block.html",
    )
    embed = EmbedBlock(
        icon="code",
        template="patterns/molecules/streamfield/blocks/embed_block.html",
        group="Media",
    )
    video_block = VideoBlock(group="Media")
    story_embed = ExternalStoryEmbedBlock(
        icon="code",
        template="patterns/molecules/streamfield/blocks/external_story_block.html",
    )

    class Meta:
        template = "patterns/molecules/streamfield/stream_block.html"


class PageSectionStoryBlock(StreamBlock):
    key_points_summary = ListBlock(
        KeyPoint(),
        icon="list-ul",
        min_num=3,
        max_num=6,
        template="patterns/molecules/streamfield/blocks/key_points_summary.html",
        help_text="Please add a minumum of 3 and a maximum of 6 key points.",
    )
    testimonials = ListBlock(
        TestimonialBlock(),
        icon="openquote",
        template="patterns/molecules/streamfield/blocks/testimonial_block.html",
    )
    clients = ListBlock(
        ImageWithLinkBlock(),
        icon="site",
        template="patterns/molecules/streamfield/blocks/client-logo-block.html",
        label="Clients logo",
    )
    embed_plus_cta = EmbedPlusCTABlock(
        label="Embed + CTA",
        icon="code",
        template="patterns/molecules/streamfield/blocks/embed_plus_cta_block.html",
    )
    cta = CTABlock(
        icon="plus-inverse",
        template="patterns/molecules/streamfield/blocks/cta.html",
    )

    class Meta:
        template = "patterns/molecules/streamfield/stream_block.html"
