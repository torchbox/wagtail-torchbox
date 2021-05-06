from django import forms
from django.db import models
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Orderable, Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from tbx.core.utils.cache import get_default_cache_control_decorator
from tbx.taxonomy.models import Service

@method_decorator(get_default_cache_control_decorator(), name="serve")
class EventIndexPage(Page):
    template = "patterns/pages/events/events_listing.html"

    subpage_types = ["EventPage"]

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular
        popular_tags = (
            EventPageTagSelect.objects.all()
            .values("tag")
            .annotate(item_count=models.Count("tag"))
            .order_by("-item_count")
        )

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [Tag.objects.get(id=tag["tag"]) for tag in popular_tags[:10]]

    @property
    def events(self):
        # Get list of event pages that are descendants of this page
        event_pages = EventPage.objects.descendant_of(self).live()

        # Order by most recent date first
        event_pages = event_pages.order_by("-date", "-pk")

        return event_pages

    def serve(self, request):
        # Get event pages
        events = self.events

        # Filter by related_service slug
        slug_filter = request.GET.get("filter")
        if slug_filter:
            events = events.filter(related_services__slug=slug_filter)

        # Pagination
        paginator = Paginator(events, 10)  # Show 10 events per page

        if request.is_ajax():
            page = request.GET.get("page")
            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                events = paginator.page(1)
            except EmptyPage:
                events = None

            return render(
                request,
                "patterns/organisms/events-listing/events-listing.html",
                {"page": self, "events": events},
            )
        else:
            # return first page contents
            try:
                events = paginator.page(1)
            except EmptyPage:
                events = None

            related_services = Service.objects.all()

            return render(
                request,
                self.template,
                {"page": self, "events": events, "related_services": related_services},
            )

    content_panels = [
        FieldPanel("title", classname="full title"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


class EventPage(Page):
    template = "patterns/pages/event/event_detail.html"

    parent_page_types = ["EventIndexPage"]

    date = models.DateField("Post date", null=True)
    event_url = models.URLField(blank=True)
    description = models.CharField(max_length=255, blank=True)
    related_services = ParentalManyToManyField(
        "taxonomy.Service", related_name="events"
    )

    @property
    def event_index(self):
        ancestor = EventIndexPage.objects.ancestor_of(self).order_by("-depth").first()

        if ancestor:
            return ancestor
        else:
            # No ancestors are event indexes,
            # just return first event index in database
            return EventIndexPage.objects.first()

    @property
    def has_authors(self):
        return self.authors.exists()

    @property
    def first_author(self):
        """Safely return the first author if one exists."""
        author = self.authors.first()
        if author:
            return author.author
        return None

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("description"),
        FieldPanel("event_url"),
        FieldPanel("date"),
        InlinePanel("authors", label="Author"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
    ]


class EventPageTagSelect(Orderable):
    page = ParentalKey("events.EventPage", related_name="tags")
    tag = models.ForeignKey(
        "torchbox.Tag", on_delete=models.CASCADE, related_name="event_page_tag_select"
    )


class EventPageAuthor(Orderable):
    page = ParentalKey("events.EventPage", related_name="authors")
    author = models.ForeignKey(
        "people.Author", on_delete=models.CASCADE, related_name="+"
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

