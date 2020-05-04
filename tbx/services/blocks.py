from grapple.helpers import register_streamfield_block
from grapple.models import (GraphQLCollection, GraphQLForeignKey, GraphQLImage,
                            GraphQLPage, GraphQLString)
from wagtail.core.blocks import (CharBlock, ListBlock, PageChooserBlock,
                                 RichTextBlock, StreamBlock, StructBlock,
                                 TextBlock, URLBlock)
from wagtail.images.blocks import ImageChooserBlock

from tbx.core.blocks import PullQuoteBlock


@register_streamfield_block
class CaseStudyLink(StructBlock):
    page = PageChooserBlock('work.WorkPage')
    title = CharBlock(required=False)
    descriptive_title = CharBlock(required=False)
    image = ImageChooserBlock(required=False)

    graphql_fields = [
        GraphQLForeignKey('page', 'work.WorkPage'),
        GraphQLString('title'),
        GraphQLString('descriptive_title'),
        GraphQLImage('image')
    ]


@register_streamfield_block
class CaseStudyBlock(StructBlock):
    title = CharBlock(required=True)
    intro = TextBlock(required=True)
    case_studies = ListBlock(CaseStudyLink())

    class Meta:
        template = 'blocks/services/case_study_block.html'

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('intro'),
        GraphQLForeignKey('case_studies', CaseStudyLink, is_list=True)
    ]


@register_streamfield_block
class HighlightBlock(StructBlock):
    title = CharBlock(required=True)
    intro = RichTextBlock(required=False)
    highlights = ListBlock(TextBlock())

    class Meta:
        template = 'blocks/services/highlight_block.html'

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('intro'),
        GraphQLCollection('highlights', GraphQLString)
    ]


@register_streamfield_block
class Step(StructBlock):
    subtitle = CharBlock(required=False)
    title = CharBlock(required=True)
    icon = CharBlock(max_length=9000, required=True, help_text='Paste SVG code here')
    description = RichTextBlock(required=True)

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('subtitle'),
        GraphQLString('icon'),
        GraphQLString('description')
    ]


@register_streamfield_block
class StepByStepBlock(StructBlock):
    title = CharBlock(required=True)
    intro = TextBlock(required=False)
    steps = ListBlock(Step())

    class Meta:
        template = 'blocks/services/step_by_step_block.html'

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('intro'),
        GraphQLForeignKey('steps', Step, is_list=True)
    ]


@register_streamfield_block
class PeopleBlock(StructBlock):
    title = CharBlock(required=True)
    intro = RichTextBlock(required=True)
    people = ListBlock(PageChooserBlock())

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('intro'),
        GraphQLCollection('people', GraphQLPage)
    ]


@register_streamfield_block
class FeaturedPage(StructBlock):
    page = PageChooserBlock()
    image = ImageChooserBlock()
    text = TextBlock()
    sub_text = CharBlock(max_length=100)


@register_streamfield_block
class FeaturedPagesBlock(StructBlock):
    title = CharBlock()
    pages = ListBlock(FeaturedPage())

    class Meta:
        template = 'blocks/services/featured_pages_block.html'

    graphql_fields = [
        GraphQLString('title'),
        GraphQLForeignKey('pages', FeaturedPage, is_list=True)
    ]


class SignUpFormPageBlock(StructBlock):
    page = PageChooserBlock('sign_up_form.SignUpFormPage')

    def get_context(self, value, parent_context=None):
        context = super(SignUpFormPageBlock, self).get_context(value, parent_context)
        context['form'] = value['page'].sign_up_form_class()

        return context

    class Meta:
        icon = 'doc-full'
        template = 'blocks/services/sign_up_form_page_block.html'


class Logo(StructBlock):
    image = ImageChooserBlock()
    link_page = PageChooserBlock(required=False)
    link_external = URLBlock(required=False)

    graphql_fields = [
        GraphQLImage('image'),
        GraphQLPage('link_page'),
        GraphQLString('link_external')
    ]


@register_streamfield_block
class LogosBlock(StructBlock):
    title = CharBlock()
    intro = CharBlock()
    logos = ListBlock(Logo)

    class Meta:
        icon = 'site'
        template = 'blocks/services/logos_block.html'

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('intro'),
        GraphQLForeignKey('logos', Logo, is_list=True),
    ]


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
