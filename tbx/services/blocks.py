from wagtail.core.blocks import (CharBlock, ListBlock, PageChooserBlock,
                                 RichTextBlock, StreamBlock, StructBlock,
                                 TextBlock, URLBlock)
from wagtail.images.blocks import ImageChooserBlock

from tbx.core.blocks import PullQuoteBlock


class CaseStudyBlock(StructBlock):
    title = CharBlock(required=True)
    intro = TextBlock(required=True)
    case_studies = ListBlock(StructBlock([
        ('page', PageChooserBlock('work.WorkPage')),
        ('title', CharBlock(required=False)),
        ('descriptive_title', CharBlock(required=False)),
        ('image', ImageChooserBlock(required=False)),
    ]))

    class Meta:
        template = 'blocks/services/case_study_block.html'


class HighlightBlock(StructBlock):
    title = CharBlock(required=True)
    intro = RichTextBlock(required=False)
    highlights = ListBlock(TextBlock())

    class Meta:
        template = 'blocks/services/highlight_block.html'


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
        template = 'blocks/services/step_by_step_block.html'


class PeopleBlock(StructBlock):
    title = CharBlock(required=True)
    intro = RichTextBlock(required=True)
    people = ListBlock(PageChooserBlock())

    class Meta:
        template = 'blocks/services/people_block.html'


class FeaturedPagesBlock(StructBlock):
    title = CharBlock()
    pages = ListBlock(StructBlock([
        ('page', PageChooserBlock()),
        ('image', ImageChooserBlock()),
        ('text', TextBlock()),
        ('sub_text', CharBlock(max_length=100)),
    ]))

    class Meta:
        template = 'blocks/services/featured_pages_block.html'


class SignUpFormPageBlock(StructBlock):
    page = PageChooserBlock('sign_up_form.SignUpFormPage')

    def get_context(self, value, parent_context=None):
        context = super(SignUpFormPageBlock, self).get_context(value, parent_context)
        context['form'] = value['page'].sign_up_form_class()

        return context

    class Meta:
        icon = 'doc-full'
        template = 'blocks/services/sign_up_form_page_block.html'


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
        template = 'blocks/services/logos_block.html'


class ServicePageBlock(StreamBlock):
    paragraph = RichTextBlock(icon="pilcrow")
    case_studies = CaseStudyBlock()
    highlights = HighlightBlock()
    pull_quote = PullQuoteBlock(template='blocks/services/pull_quote_block.html')
    process = StepByStepBlock()
    people = PeopleBlock()
    featured_pages = FeaturedPagesBlock()
    sign_up_form_page = SignUpFormPageBlock()
    logos = LogosBlock()
