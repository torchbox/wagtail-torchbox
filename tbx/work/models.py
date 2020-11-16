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
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from tbx.core.blocks import StoryBlock
from tbx.core.models import Tag
from tbx.core.utils.cache import get_default_cache_control_decorator
from tbx.taxonomy.models import Service


# Currently hidden. These were used in the past and may be used again in the future
class WorkPageTagSelect(Orderable):
    page = ParentalKey("work.WorkPage", related_name="tags")
    tag = models.ForeignKey(
        "torchbox.Tag", on_delete=models.CASCADE, related_name="work_page_tag_select"
    )


class WorkPageScreenshot(Orderable):
    page = ParentalKey("work.WorkPage", related_name="screenshots")
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        ImageChooserPanel("image"),
    ]


class WorkPageAuthor(Orderable):
    page = ParentalKey("work.WorkPage", related_name="authors")
    author = models.ForeignKey(
        "people.Author", on_delete=models.CASCADE, related_name="+"
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class WorkPage(Page):
    template = "patterns/pages/work/work_detail.html"

    body = StreamField(StoryBlock())
    body_word_count = models.PositiveIntegerField(null=True, editable=False)
    homepage_image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    visit_the_site = models.URLField(blank=True)

    feed_image = models.ForeignKey(
        "torchbox.TorchboxImage",
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
            return WorkIndexPage.objects.first()

    @property
    def has_authors(self):
        return self.authors.exists()

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
        return math.ceil(self.body_word_count / 275)

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("client", classname="client"),
        InlinePanel("authors", label="Author"),
        StreamFieldPanel("body"),
        ImageChooserPanel("homepage_image"),
        InlinePanel("screenshots", label="Screenshots"),
        FieldPanel("visit_the_site"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel("feed_image"),
        FieldPanel("listing_summary"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
    ]


# Work index page
@method_decorator(get_default_cache_control_decorator(), name="serve")
class WorkIndexPage(Page):
    template = "patterns/pages/work/work_listing.html"

    intro = RichTextField(blank=True)

    hide_popular_tags = models.BooleanField(default=False)

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
        return WorkPage.objects.descendant_of(self).live()

    def serve(self, request):
        # Get work pages
        works = self.works

        # Filter by related_service slug
        slug_filter = request.GET.get("filter")
        if slug_filter:
            works = works.filter(related_services__slug=slug_filter)

        # Pagination
        paginator = Paginator(works, 10)  # Show 10 works per page

        if request.is_ajax():
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

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("intro", classname="full"),
        FieldPanel("hide_popular_tags"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


@receiver(page_published, sender=WorkPage)
def update_body_word_count_on_page_publish(instance, **kwargs):
    instance.set_body_word_count()
    instance.save(update_fields=["body_word_count"])
