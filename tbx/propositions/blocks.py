from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from tbx.core import blocks as core_blocks
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.snippets import blocks as snippet_blocks


class KeyPointBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=255)
    linked_page = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = "check"
        label = "Key point"


class KeyPointsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label="Key points section title",
        max_length=255,
        default="Services",
    )
    heading_for_key_points = blocks.RichTextBlock(
        required=False,
    )
    key_points = blocks.ListBlock(
        KeyPointBlock(),
    )
    contact = snippet_blocks.SnippetChooserBlock(
        "people.Contact",
        required=False,
    )
    contact_reasons = snippet_blocks.SnippetChooserBlock(
        "people.ContactReasonsList",
        required=False,
    )

    class Meta:
        icon = "list-ul"
        label = "Key points"
        template = "patterns/molecules/streamfield/blocks/key-points.html"


class TestimonialsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label="Testimonials section title",
        max_length=255,
        default="Clients",
    )
    client_logos = blocks.ListBlock(
        core_blocks.ImageWithLinkBlock(),
        required=False,
    )
    testimonials = blocks.ListBlock(
        core_blocks.TestimonialBlock(),
        required=False,
    )

    class Meta:
        icon = "openquote"
        label = "Testimonials"
        template = "patterns/molecules/streamfield/blocks/testimonials.html"


class LinkStructValue(blocks.StructValue):
    def link(self):
        if page := self.get("page_link"):
            return page.get_url()
        if external_link := self.get("external_link"):
            return external_link


class ProcessBlock(blocks.StructBlock):
    title = blocks.TextBlock()
    description = blocks.TextBlock()
    external_link = blocks.URLBlock(required=False)
    page_link = blocks.PageChooserBlock(required=False)
    link_label = blocks.CharBlock(required=False)

    def clean(self, value):
        struct_value = super().clean(value)

        errors = {}
        page_link = value.get("page_link")
        external_link = value.get("external_link")

        if page_link and external_link:
            error = ErrorList(
                [
                    ValidationError(
                        "Either a page or an external link may be specified, but not both."
                    )
                ]
            )
            errors["page_link"] = errors["external_link"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value

    class Meta:
        icon = "pick"
        label = "Process"
        value_class = LinkStructValue


class ProcessesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label="Process section title",
        default="Process",
    )
    processes = blocks.ListBlock(ProcessBlock())
    process_section_cta = blocks.RichTextBlock(
        label="Process section CTA",
        required=False,
        help_text="An opportunity to use a more flexible call to action, if the main “Contact” fields aren’t suitable",
    )

    class Meta:
        icon = "pick"
        label = "Processes"
        template = "patterns/molecules/streamfield/blocks/process-section.html"


class WorkBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label="Case studies section title",
        default="Work",
    )
    featured_case_studies = blocks.ListBlock(
        blocks.PageChooserBlock(
            page_type="work.WorkPage",
        )
    )

    def get_featured_case_studies(self, value):
        """Format the featured case studies data for the template."""
        return [
            {
                "title": case_study.title,
                "subtitle": case_study.client,
                "description": case_study.listing_summary,
                "url": case_study.url,
                "image": case_study.homepage_image,
            }
            for case_study in value.get("featured_case_studies")
            if case_study
        ]

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["featured_case_studies"] = self.get_featured_case_studies(value)
        return context

    class Meta:
        icon = "folder-open-inverse"
        label = "Work"
        template = "patterns/molecules/streamfield/blocks/case_studies_section.html"


class ThinkingBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label="Blogs section title",
        default="Thinking",
    )
    featured_blog_posts = blocks.ListBlock(
        blocks.PageChooserBlock(
            page_type="blog.BlogPage",
        )
    )

    def get_featured_blog_posts(self, value):
        """Format the featured blog posts for the template."""
        return [
            {
                "title": blog_post.title,
                "url": blog_post.url,
                "author": blog_post.first_author,
                "date": blog_post.date,
            }
            for blog_post in value.get("featured_blog_posts")
            if blog_post and blog_post.live
        ]

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["featured_blog_posts"] = self.get_featured_blog_posts(value)
        return context

    class Meta:
        icon = "pilcrow"
        label = "Thinking"
        template = "patterns/molecules/streamfield/blocks/thinking.html"


class SubPropositionPageStoryBlock(blocks.StreamBlock):
    # Page sections (headings appear in the in-page-nav in hero)
    key_points = KeyPointsBlock(
        group="Page section",
    )
    testimonials = TestimonialsBlock(
        label="Testimonials / Clients logos",
        group="Page section",
    )
    processes = ProcessesBlock(
        group="Page section",
    )
    work = WorkBlock(
        group="Page section",
    )
    thinking = ThinkingBlock(
        group="Page section",
    )

    # These are from tbx.core.blocks.PageSectionStoryBlock
    embed_plus_cta = core_blocks.EmbedPlusCTABlock(
        label="Embed + CTA",
        icon="code",
        template="patterns/molecules/streamfield/blocks/embed_plus_cta_block.html",
        group="Call to action",
    )
    cta = core_blocks.CTABlock(
        label="CTA",
        icon="plus-inverse",
        template="patterns/molecules/streamfield/blocks/cta.html",
        group="Call to action",
    )

    @staticmethod
    def get_section_block_types():
        return [
            "key_points",
            "testimonials",
            "processes",
            "work",
            "thinking",
        ]

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["section_block_types"] = self.get_section_block_types()
        return context

    class Meta:
        template = "patterns/molecules/streamfield/sub_proposition_stream_block.html"
