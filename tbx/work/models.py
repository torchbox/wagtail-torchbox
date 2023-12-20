import math
import string

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.dispatch import receiver
from django.shortcuts import render
from django.utils.decorators import method_decorator

from bs4 import BeautifulSoup
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from tbx.core.blocks import PageSectionStoryBlock, StoryBlock
from tbx.core.models import Tag
from tbx.core.utils.cache import get_default_cache_control_decorator
from tbx.core.utils.models import SocialFields
from tbx.taxonomy.models import Service
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.signals import page_published


# Currently hidden. These were used in the past and may be used again in the future
class WorkPageTagSelect(Orderable):
    page = ParentalKey("work.WorkPage", related_name="tags")
    tag = models.ForeignKey(
        "torchbox.Tag", on_delete=models.CASCADE, related_name="work_page_tag_select"
    )


class WorkPageScreenshot(Orderable):
    page = ParentalKey("work.WorkPage", related_name="screenshots")
    image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("image"),
    ]


class WorkPageAuthor(Orderable):
    page = ParentalKey("work.WorkPage", related_name="authors")
    author = models.ForeignKey(
        "people.Author", on_delete=models.CASCADE, related_name="+"
    )

    panels = [
        FieldPanel("author"),
    ]


class WorkPage(SocialFields, Page):
    template = "patterns/pages/work/work_detail.html"

    parent_page_types = ["WorkIndexPage"]

    date = models.DateField("Post date", blank=True, null=True)
    body = StreamField(StoryBlock(), use_json_field=True)
    body_word_count = models.PositiveIntegerField(null=True, editable=False)
    homepage_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    visit_the_site = models.URLField(blank=True)

    feed_image = models.ForeignKey(
        "images.CustomImage",
        help_text="Image used on listings and social media.",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    listing_summary = models.CharField(max_length=255, blank=True)
    related_services = ParentalManyToManyField(
        "taxonomy.Service", related_name="case_studies"
    )
    client = models.TextField(blank=True)

    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
    )

    def set_body_word_count(self):
        body_basic_html = self.body.stream_block.render_basic(self.body)
        body_text = BeautifulSoup(body_basic_html, "html.parser").get_text()
        remove_chars = string.punctuation + "“”’"
        body_words = body_text.translate(
            body_text.maketrans(dict.fromkeys(remove_chars))
        ).split()
        self.body_word_count = len(body_words)

    @property
    def work_index(self):
        ancestor = WorkIndexPage.objects.ancestor_of(self).order_by("-depth").first()

        if ancestor:
            return ancestor
        else:
            # No ancestors are work indexes,
            # just return first work index in database
            return WorkIndexPage.objects.live().public().first()

    @property
    def first_author(self):
        """Safely return the first author if one exists."""
        author = self.authors.first()
        if author:
            return author.author
        return None

    @property
    def related_works(self):
        services = self.related_services.all()
        # get 4 pages with same services and exclude self page
        works = (
            WorkPage.objects.filter(related_services__in=services)
            .live()
            .distinct()
            .order_by("-id")
            .exclude(pk=self.pk)[:4]
        )
        return works

    @property
    def read_time(self):
        if self.body_word_count:
            return math.ceil(self.body_word_count / 275)
        else:
            return "x"

    @property
    def type(self):
        return "CASE STUDY"

    content_panels = Page.content_panels + [
        FieldPanel("client", classname="client"),
        InlinePanel("authors", label="Author", min_num=1),
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("homepage_image"),
        InlinePanel("screenshots", label="Screenshots"),
        FieldPanel("visit_the_site"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("feed_image"),
        FieldPanel("listing_summary"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]


# Work index page
@method_decorator(get_default_cache_control_decorator(), name="serve")
class WorkIndexPage(SocialFields, Page):
    template = "patterns/pages/work/work_listing.html"

    subpage_types = ["WorkPage"]

    intro = RichTextField(blank=True)

    hide_popular_tags = models.BooleanField(default=False)

    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
    )

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular
        popular_tags = (
            WorkPageTagSelect.objects.all()
            .values("tag")
            .annotate(item_count=models.Count("tag"))
            .order_by("-item_count")
        )

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [Tag.objects.get(id=tag["tag"]) for tag in popular_tags[:10]]

    @property
    def works(self):
        # Get list of work pages that are descendants of this page
        work_pages = WorkPage.objects.descendant_of(self).live()

        # Order by most recent date first
        work_pages = work_pages.order_by("-date", "-pk")

        return work_pages

    def serve(self, request):
        # Get work pages
        works = self.works

        # Filter by related_service slug
        slug_filter = request.GET.get("filter")
        if slug_filter:
            works = works.filter(related_services__slug=slug_filter)

        # format for template
        works = [
            {
                "title": work.title,
                "subtitle": work.client,
                "description": work.listing_summary,
                "url": work.url,
                "image": work.homepage_image,
            }
            for work in works
        ]

        # Pagination
        paginator = Paginator(works, 10)  # Show 10 works per page

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            page = request.GET.get("page")
            try:
                works = paginator.page(page)
            except PageNotAnInteger:
                works = paginator.page(1)
            except EmptyPage:
                works = None

            return render(
                request,
                "patterns/organisms/work-listing/work-listing.html",
                {"page": self, "works": works},
            )
        else:
            # return first page contents
            try:
                works = paginator.page(1)
            except EmptyPage:
                works = None

            related_services = Service.objects.all()

            return render(
                request,
                self.template,
                {"page": self, "works": works, "related_services": related_services},
            )

    def serve_preview(self, request, mode_name):
        return self.serve(request)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("hide_popular_tags"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]


@receiver(page_published, sender=WorkPage)
def update_body_word_count_on_page_publish(instance, **kwargs):
    instance.set_body_word_count()
    instance.save(update_fields=["body_word_count"])
