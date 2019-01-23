from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from .blocks import ServicePageBlock


class ServiceIndexPageService(Orderable):
    page = ParentalKey('services.ServiceIndexPage', related_name='services')
    title = models.TextField()
    svg = models.TextField(null=True)
    description = models.TextField()
    link = models.ForeignKey(
        'services.ServicePage',
        related_name='+',
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        PageChooserPanel('link'),
        FieldPanel('svg')
    ]


class ServiceIndexPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading = models.TextField(blank=True)
    intro = models.TextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        FieldPanel('heading'),
        FieldPanel('intro', classname='full'),
        InlinePanel('services', label='Services'),
    ]


class ServicePage(Page):
    description = models.TextField()
    streamfield = StreamField(ServicePageBlock())
    particle = models.ForeignKey(
        'torchbox.ParticleSnippet',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('description', classname="full"),
        StreamFieldPanel('streamfield'),
        FieldPanel('particle'),
    ]
