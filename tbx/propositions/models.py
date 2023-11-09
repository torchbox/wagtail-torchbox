import logging

from django.db import models
from django.utils.functional import cached_property

from tbx.blog.models import BlogIndexPage
from tbx.core.blocks import PageSectionStoryBlock
from tbx.core.utils.models import SocialFields
from tbx.propositions.blocks import (
    SubPropositionPageStoryBlock,
    ThinkingBlock,
    WorkBlock,
)
from tbx.work.models import WorkIndexPage
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

logger = logging.getLogger(__name__)

INTRO_RICHTEXT_FEATURES = ["bold", "italic", "link", "document-link", "strikethrough"]


class PropositionPage(SocialFields, Page):
    template = "patterns/pages/proposition/proposition.html"

    subpage_types = [
        "torchbox.StandardPage",
        "services.SubServicePage",
        "propositions.SubPropositionPage",
    ]

    service = models.OneToOneField(
        "taxonomy.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Link to this service in taxonomy",
    )

    theme = models.CharField(
        max_length=255,
        choices=(
            ("light", "Light"),
            ("coral", "Coral"),
            ("dark", "Dark"),
        ),
        default="light",
    )

    # Hero section
    strapline = models.CharField(
        max_length=255,
        help_text="Words in <span> tag will display in a contrasting colour.",
    )
    intro = RichTextField(blank=True, features=INTRO_RICHTEXT_FEATURES)
    image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Service section
    services_section_title = models.CharField(blank=True, max_length=255)
    services_section_intro = RichTextField(blank=True, features=INTRO_RICHTEXT_FEATURES)
    services_section_body = StreamField(
        PageSectionStoryBlock(), blank=True, use_json_field=True, collapsed=True
    )

    # Our clients section
    clients_section_title = models.CharField(blank=True, max_length=255)
    clients_section_intro = RichTextField(blank=True, features=INTRO_RICHTEXT_FEATURES)
    clients_section_body = StreamField(
        PageSectionStoryBlock(), blank=True, use_json_field=True, collapsed=True
    )

    # Team section
    team_section_title = models.CharField(blank=True, max_length=255)
    team_section_intro = RichTextField(blank=True, features=INTRO_RICHTEXT_FEATURES)
    team_section_body = StreamField(
        PageSectionStoryBlock(), blank=True, use_json_field=True, collapsed=True
    )

    # Our thinking section
    our_thinking_section_body = StreamField(
        [
            ("our_thinking", ThinkingBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    # Our work section
    our_work_section_body = StreamField(
        [
            ("our_work", WorkBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    search_fields = Page.search_fields + [
        index.SearchField("service"),
        index.SearchField("intro"),
        index.SearchField("strapline"),
        index.SearchField("services_section_title"),
        index.SearchField("services_section_intro"),
        index.SearchField("services_section_body"),
        index.SearchField("clients_section_title"),
        index.SearchField("clients_section_intro"),
        index.SearchField("clients_section_body"),
        index.SearchField("team_section_title"),
        index.SearchField("team_section_intro"),
        index.SearchField("team_section_body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("service"),
        FieldPanel("theme"),
        MultiFieldPanel(
            [
                FieldPanel("strapline", classname="full title"),
                FieldPanel("intro", classname="full"),
                FieldPanel("image"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("services_section_title", heading="Title"),
                FieldPanel("services_section_intro", heading="Intro", classname="full"),
                FieldPanel("services_section_body", heading="Content"),
            ],
            heading="Services",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("clients_section_title", heading="Title"),
                FieldPanel("clients_section_intro", heading="Intro", classname="full"),
                FieldPanel("clients_section_body", heading="Content"),
            ],
            heading="Our clients",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("team_section_title", heading="Title"),
                FieldPanel("team_section_intro", heading="Intro", classname="full"),
                FieldPanel("team_section_body", heading="Content"),
            ],
            heading="Our team",
            classname="collapsible",
        ),
        FieldPanel("our_work_section_body"),
        FieldPanel("our_thinking_section_body"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    @property
    def section_titles(self):
        section_titles = [
            "Services",
            "Our clients",
            "Our team",
        ]

        if self.our_work_section_body:
            section_titles.append("Work")

        if self.our_thinking_section_body:
            section_titles.append("Thinking")

        return section_titles

    @property
    def filter_by(self):
        if self.service:
            return self.service.slug

        # If no service defined, don't filter by anything
        return ""

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            blog_index_page=BlogIndexPage.objects.live().first(),
            work_index_page=WorkIndexPage.objects.live().first(),
        )
        return context


class SubPropositionPage(SocialFields, Page):
    template = "patterns/pages/proposition/sub_proposition.html"
    # TODO: remove "ServicePage" from the list when deprecating ServicePage
    parent_page_types = ["services.ServicePage", "propositions.PropositionPage"]
    subpage_types = ["torchbox.StandardPage"]

    theme = models.CharField(
        max_length=255,
        choices=(
            ("light", "Light"),
            ("coral", "Coral"),
            ("dark", "Dark"),
        ),
        default="light",
    )

    strapline = models.CharField(
        max_length=255,
        help_text="Words in <span> tag will display in a contrasting colour.",
    )
    intro = RichTextField(blank=True)
    greeting_image_type = models.CharField(
        max_length=255,
        choices=(
            ("woman-left", "Woman (Left Aligned)"),
            ("man-left", "Man (Left aligned)"),
            ("wagtail", "Wagtail (Right aligned)"),
        ),
        default="woman-left",
        blank=True,
        null=True,
    )

    content = StreamField(
        SubPropositionPageStoryBlock(), blank=True, use_json_field=True, collapsed=True
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("theme"),
        MultiFieldPanel(
            [
                FieldPanel("strapline", classname="title"),
                FieldPanel("intro"),
                FieldPanel("greeting_image_type"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        FieldPanel("content"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    @cached_property
    def section_titles(self):
        """
        We need these in order to render the in-page-nav in the hero
        """
        block_types = SubPropositionPageStoryBlock.get_section_block_types()
        try:
            section_titles = [
                block.value["title"]
                for block in self.content
                if block.block_type in block_types
            ]
            return section_titles
        except AttributeError:
            logger.exception(
                f"Error getting section titles from SubPropositionPage {self.pk}"
            )
            return []

    @cached_property
    def service(self):
        proposition_page = (
            PropositionPage.objects.ancestor_of(self)
            .defer_streamfields()
            .select_related("service")
            .last()
        )

        if proposition_page and hasattr(proposition_page, "service"):
            return proposition_page.service

        return None

    @property
    def filter_by(self):
        if self.service:
            return self.service.slug

        # If no service defined, don't filter by anything
        return ""

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            blog_index_page=BlogIndexPage.objects.live().first(),
            work_index_page=WorkIndexPage.objects.live().first(),
        )
        return context


class SubServicePageToSubPropositionPageMigration(models.Model):
    """
    Keep track of changes to simplify rollback if needed.

    NOTE: This can be removed once we are confident that all content
    has been successfully migrated and everything is working as expected.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    subservice_page = models.ForeignKey(
        "services.SubServicePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    subservice_page_was_live = models.BooleanField(
        default=True,
        editable=False,
    )
    subproposition_page = models.ForeignKey(
        "propositions.SubPropositionPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def __str__(self):
        return (
            f"SubServicePage {self.subservice_page.pk} → "
            f"SubPropositionPage {self.subproposition_page.pk}"
        )
