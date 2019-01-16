from django import forms

from wagtail.core.blocks import (CharBlock, FieldBlock, ListBlock,
                                 PageChooserBlock, RawHTMLBlock, RichTextBlock,
                                 StreamBlock, StructBlock, TextBlock, URLBlock)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'),
        ('right', 'Wrap right'),
        ('half', 'Half width'),
        ('full', 'Full width'),
    ))


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


# Service Page

class CaseStudyBlock(StructBlock):
    title = CharBlock(required=True)
    intro = TextBlock(required=True)
    case_studies = ListBlock(StructBlock([
        ('page', PageChooserBlock('torchbox.WorkPage')),
        ('title', CharBlock(required=False)),
        ('descriptive_title', CharBlock(required=False)),
        ('image', ImageChooserBlock(required=False)),
    ]))

    class Meta:
        template = 'blocks/case_study_block.html'


class HighlightBlock(StructBlock):
    title = CharBlock(required=True)
    intro = RichTextBlock(required=False)
    highlights = ListBlock(TextBlock())

    class Meta:
        template = 'blocks/highlight_block.html'


class StepByStepBlock(StructBlock):
    title = CharBlock(required=True)
    intro = TextBlock(required=False)
    steps = ListBlock(StructBlock([
        ('subtitle', CharBlock(required=False)),
        ('title', CharBlock(required=True)),
        ('icon', CharBlock(max_length=9000, required=True, help_text='Paste SVG code here')),
        ('description', RichTextBlock(required=True))
    ]))

    class Meta:
        template = 'blocks/step_by_step_block.html'


class PeopleBlock(StructBlock):
    title = CharBlock(required=True)
    intro = RichTextBlock(required=True)
    people = ListBlock(PageChooserBlock())

    class Meta:
        template = 'blocks/people_block.html'


class FeaturedPagesBlock(StructBlock):
    title = CharBlock()
    pages = ListBlock(StructBlock([
        ('page', PageChooserBlock()),
        ('image', ImageChooserBlock()),
        ('text', TextBlock()),
        ('sub_text', CharBlock(max_length=100)),
    ]))

    class Meta:
        template = 'blocks/featured_pages_block.html'


class SignUpFormPageBlock(StructBlock):
    page = PageChooserBlock('torchbox.SignUpFormPage')

    def get_context(self, value, parent_context=None):
        context = super(SignUpFormPageBlock, self).get_context(value, parent_context)
        context['form'] = value['page'].sign_up_form_class()

        return context

    class Meta:
        icon = 'doc-full'
        template = 'blocks/sign_up_form_page_block.html'


class LogosBlock(StructBlock):
    title = CharBlock()
    intro = CharBlock()
    logos = ListBlock(StructBlock((
        ('image', ImageChooserBlock()),
        ('link_page', PageChooserBlock(required=False)),
        ('link_external', URLBlock(required=False)),
    )))

    class Meta:
        icon = 'site'
        template = 'blocks/logos_block.html'


class ServicePageBlock(StreamBlock):
    paragraph = RichTextBlock(icon="pilcrow")
    case_studies = CaseStudyBlock()
    highlights = HighlightBlock()
    pull_quote = PullQuoteBlock(template='blocks/pull_quote_block.html')
    process = StepByStepBlock()
    people = PeopleBlock()
    featured_pages = FeaturedPagesBlock()
    sign_up_form_page = SignUpFormPageBlock()
    logos = LogosBlock()
