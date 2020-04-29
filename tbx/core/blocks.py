from django import forms

from wagtail.core.blocks import (CharBlock, FieldBlock, ListBlock,
                                 RawHTMLBlock, RichTextBlock, StreamBlock,
                                 StructBlock)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock
from grapple.models import GraphQLString, GraphQLForeignKey, GraphQLImage
from grapple.helpers import register_streamfield_block


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'),
        ('right', 'Wrap right'),
        ('half', 'Half width'),
        ('full', 'Full width'),
    ))

    graphql_fields = [
        GraphQLString('field')
    ]


@register_streamfield_block
class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alignment = ImageFormatChoiceBlock()
    caption = CharBlock()
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"

    graphql_fields = [
        GraphQLImage('image'),
        GraphQLString("alignment"),
        GraphQLString('caption'),
        GraphQLString('attribution'),
    ]


@register_streamfield_block
class PhotoGridBlock(StructBlock):
    images = ListBlock(ImageChooserBlock())

    class Meta:
        icon = "grip"


@register_streamfield_block
class PullQuoteBlock(StructBlock):
    quote = CharBlock(classname="quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

    graphql_fields = [
        GraphQLString('quote'),
        GraphQLString('attribution'),
    ]


@register_streamfield_block
class PullQuoteImageBlock(StructBlock):
    quote = CharBlock()
    attribution = CharBlock()
    image = ImageChooserBlock(required=False)

    graphql_fields = [
        GraphQLString('quote'),
        GraphQLString('attribution'),
        GraphQLImage('image'),
    ]


@register_streamfield_block
class BustoutBlock(StructBlock):
    image = ImageChooserBlock()
    text = RichTextBlock()

    class Meta:
        icon = "pick"

    graphql_fields = [
        GraphQLImage('image'),
        GraphQLString('text'),
    ]


@register_streamfield_block
class WideImage(StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"

    graphql_fields = [
        GraphQLImage('image')
    ]


class StatsBlock(StructBlock):
    pass

    class Meta:
        icon = "order"


class StoryBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image")
    wide_image = WideImage(label="Wide image")
    bustout = BustoutBlock()
    pullquote = PullQuoteBlock()
    raw_html = RawHTMLBlock(label='Raw HTML', icon="code")
    embed = EmbedBlock(icon="code")
    markdown = MarkdownBlock(icon="code")
