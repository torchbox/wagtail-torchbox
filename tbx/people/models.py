from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

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
    strapline = models.CharField(max_length=255)

    @cached_property
    def people(self):
        return PersonPage.objects.exclude(is_senior=True).live().public()

    @cached_property
    def senior_management(self):
        return PersonPage.objects.exclude(is_senior=False).live().public()

    content_panels = Page.content_panels + [
        FieldPanel('strapline', classname="full"),
    ]


# An author snippet which keeps a copy of a person's details in case they leave and their page is unpublished
# Could also be used for external authors
@register_snippet
class Author(index.Indexed, models.Model):
    person_page = models.OneToOneField('people.PersonPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def update_manual_fields(self, person_page):
        self.name = person_page.title
        self.role = person_page.role
        self.image = person_page.image

    def clean(self):
        if not self.person_page and not self.name:
            raise ValidationError({'person_page': "You must set either 'Person page' or 'Name'"})

        if self.person_page:
            self.update_manual_fields(self.person_page)

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField('name'),
    ]

    panels = [
        PageChooserPanel('person_page'),
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('role'),
            ImageChooserPanel('image'),
        ], "Manual fields"),
    ]


@receiver(page_published, sender=PersonPage)
def update_author_on_page_publish(instance, **kwargs):
    author, created = Author.objects.get_or_create(person_page=instance)
    author.update_manual_fields(instance)
    author.save()


@register_snippet
class Contact(index.Indexed, models.Model):
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    email_address = models.EmailField()
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField('name'),
    ]

    panels = [
        FieldPanel('name'),
        FieldPanel('role'),
        ImageChooserPanel('image'),
        FieldPanel('email_address'),
        FieldPanel('phone_number'),
   ]
