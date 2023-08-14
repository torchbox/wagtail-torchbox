import datetime

from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from tbx.core.blocks import PageSectionStoryBlock
from tbx.core.utils.models import SocialFields
from tbx.taxonomy.models import Service
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page


class EventIndexPage(SocialFields, Page):
    template = "patterns/pages/events/events_listing.html"

    parent_page_types = ["torchbox.HomePage"]
    subpage_types = []

    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
    )

    content_panels = Page.content_panels + [
        InlinePanel("events", label="events"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
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


class Event(ClusterableModel, Orderable):
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
        FieldPanel("author"),
        FieldPanel("date"),
        FieldPanel("event_type"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
    ]
