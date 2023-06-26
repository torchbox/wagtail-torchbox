from django.db import models

from tbx.core.blocks import PageSectionStoryBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

INTRO_RICHTEXT_FEATURES = ["bold", "italic", "link", "document-link", "strikethrough"]


class PropositionPage(Page):
    template = "patterns/pages/proposition/proposition.html"

    subpage_types = [
        "torchbox.StandardPage",
        "services.SubServicePage",
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
    ]
