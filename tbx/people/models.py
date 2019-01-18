from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from tbx.core.models import ContactFields, RelatedLink


class PersonPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('people.PersonPage', related_name='related_links')


class PersonPage(Page, ContactFields):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    is_senior = models.BooleanField(default=False)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    short_biography = models.CharField(
        max_length=255, blank=True,
        help_text='A shorter summary biography for including in other pages'
    )
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('biography'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('role'),
        FieldPanel('is_senior'),
        FieldPanel('intro', classname="full"),
        FieldPanel('biography', classname="full"),
        FieldPanel('short_biography', classname="full"),
        ImageChooserPanel('image'),
        MultiFieldPanel(ContactFields.panels, "Contact"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]


# Person index
class PersonIndexPage(Page):
    intro = models.TextField()
    senior_management_intro = models.TextField()
    team_intro = models.TextField()

    @cached_property
    def people(self):
        return PersonPage.objects.exclude(is_senior=True).live().public()

    @cached_property
    def senior_management(self):
        return PersonPage.objects.exclude(is_senior=False).live().public()

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('senior_management_intro', classname="full"),
        FieldPanel('team_intro', classname="full"),
    ]
