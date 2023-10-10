from django.db import models
from django.utils.text import slugify

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    TitleFieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from .blocks import ImpactReportStoryBlock


class ImpactReportAuthor(Orderable):
    page = ParentalKey("impact_reports.ImpactReportPage", related_name="authors")
    author = models.ForeignKey(
        "people.Author",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("author"),
    ]


class ImpactReportPage(Page):
    template = "patterns/pages/impact_reports/impact_report_page.html"

    strapline = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This is for the illustration only. Use an image with dimensions of 571x700",
    )

    introduction_title = models.CharField(max_length=255, default="Introduction")
    introduction = RichTextField(blank=True)

    body = StreamField(ImpactReportStoryBlock(), use_json_field=True)

    content_panels = [
        MultiFieldPanel(
            [
                TitleFieldPanel("title"),
                FieldPanel("strapline"),
                FieldPanel("hero_image"),
            ],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("introduction_title"),
                FieldPanel("introduction"),
                InlinePanel("authors", label="Author", min_num=1),
            ],
            heading="Introduction",
        ),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    @property
    def headings(self):
        """
        Gets all of the impact report headers' short headings and their slugs,
        including the Introduction.

        This is used to create a table-of-contents like section at the top of
        the page where viewers can jump to the top of each impact report heading
        and Introduction.
        """

        headings = [
            {
                "short_heading": self.introduction_title,
                "slug": slugify(self.introduction_title),
            },
        ]

        for block in self.body:
            if block.block_type == "impact_report_heading":
                headings.append(
                    {
                        "short_heading": block.value["short_heading"],
                        "slug": slugify(block.value["short_heading"]),
                    }
                )

        return headings
