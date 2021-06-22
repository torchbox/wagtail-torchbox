import datetime

from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import (
    Orderable,
    Page,
    ParentalKey,
    ParentalManyToManyField,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from tbx.taxonomy.models import Service


class EventIndexPage(Page):
    template = "patterns/pages/events/events_listing.html"

    parent_page_types = ["torchbox.HomePage"]
    subpage_types = []

    content_panels = [
        FieldPanel("title", classname="full title"),
        InlinePanel("events", label="events"),
    ]

    def get_events(self, service_filter=None):
        today = datetime.date.today()
        events = self.events.exclude(date__lt=today)
        if service_filter:
            events = events.filter(related_services__slug=service_filter)
        return events.order_by("date")

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            events=self.get_events(request.GET.get("filter")),
            related_services=Service.objects.all(),
        )
        return context


class Event(Orderable):
    page = ParentalKey(EventIndexPage, related_name="events")
    title = models.CharField(max_length=255)
    intro = models.TextField(verbose_name="Description")
    link_external = models.URLField("External link")
    date = models.DateField("Event date")
    event_type = models.CharField(max_length=30)
    author = models.ForeignKey(
        "people.Author",
        on_delete=models.SET_NULL,
        null=True,
        related_name="authors",
        verbose_name="Host",
    )
    related_services = ParentalManyToManyField(
        "taxonomy.Service", related_name="events"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("intro"),
        FieldPanel("link_external"),
        SnippetChooserPanel("author"),
        FieldPanel("date"),
        FieldPanel("event_type"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
    ]
