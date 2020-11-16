from django import forms

from wagtail.core.blocks import (
    CharBlock,
    FieldBlock,
    ListBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock


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


class PhotoGridBlock(StructBlock):
    images = ListBlock(ImageChooserBlock())

    class Meta:
        icon = "grip"


class PullQuoteBlock(StructBlock):
    quote = CharBlock(classname="quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class PullQuoteImageBlock(StructBlock):
    quote = CharBlock()
    attribution = CharBlock()
    image = ImageChooserBlock(required=False)


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


class StoryBlock(StreamBlock):
    h2 = CharBlock(
        classname="title",
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading2_block.html",
    )
    h3 = CharBlock(
        classname="title",
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading3_block.html",
    )
    h4 = CharBlock(
        classname="title",
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
    embed = EmbedBlock(
        icon="code",
        template="patterns/molecules/streamfield/blocks/embed_block.html",
    )
    markdown = MarkdownBlock(
        icon="code",
        template="patterns/molecules/streamfield/blocks/markdown_block.html",
    )

    class Meta:
        template = "patterns/molecules/streamfield/stream_block.html"
