from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from headlesspreview.models import HeadlessPreviewMixin
from tbx.core.blocks import StoryBlock
from tbx.core.models import ContactFields, RelatedLink
# from .fields import ZoomMeetingsField
from .events import ZoomMeetingEvent


class ZoomEventBlock(blocks.StructBlock):
  meeting_ID = blocks.CharBlock()

class EventsPage(HeadlessPreviewMixin, Page):
    strapline = models.TextField(blank=True)
    body = StreamField(StoryBlock(), blank=True)
    post_registration_body = StreamField(StoryBlock(), blank=True)
    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        help_text='Image used on listings and social media.',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Allow to choose between multiple events, to be expanded for on site too!
    event_type = StreamField(blocks.StreamBlock(
        [
            ("zoom_meeting", ZoomEventBlock()),
            ("zoom_webinar", ZoomEventBlock()),
        ],
        max_num=1,
        required=True,
    ), blank=True)

    search_fields = Page.search_fields + []

    content_panels = [
      FieldPanel('title', classname="full title"),
      FieldPanel('strapline', classname="full title"),
      MultiFieldPanel(
          [InlinePanel(('hosts'), label="Host")],
          heading="Event Hosts",
      ),
      StreamFieldPanel('event_type'),
      StreamFieldPanel('body'),
      StreamFieldPanel('post_registration_body'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]

    @property
    def event(self):
      if self.event_type.stream_data:
        # Get event setting
        event = self.event_type.stream_data[0]
        # Check event type
        if event['type'] == "zoom_meeting":
          return ZoomMeetingEvent.query_with_meeting_id(event['value']['meeting_ID'])
        if event['type'] == "zoom_webinar":
          return ZoomMeetingEvent.query_with_webinar_id(event['value']['meeting_ID'])



class EventsPageHost(Orderable):
  page = ParentalKey("events.EventsPage", related_name="hosts")
  person = models.ForeignKey(
      'people.Author',
      on_delete=models.CASCADE,
      related_name='+',
  )

  content_panels = [
      SnippetChooserPanel('person'),
  ]

