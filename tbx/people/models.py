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
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from grapple.utils import resolve_queryset
from grapple.models import (
    GraphQLString, GraphQLBoolean, GraphQLImage, GraphQLForeignKey,
    GraphQLCollection, GraphQLStreamfield, GraphQLPage
)
from tbx.core.blocks import StoryBlock
from tbx.core.models import ContactFields, RelatedLink
from tbx.utils.models import TorchboxPage
from tbx.blog.models import BlogPage


class PersonPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('people.PersonPage', related_name='related_links')


class PersonPage(TorchboxPage, ContactFields):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    is_senior = models.BooleanField(default=False)
    short_intro = models.TextField(blank=True, null=True)
    alt_short_intro = models.TextField(blank=True, null=True)
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

    def blog_posts(self, info, **kwargs):
        return resolve_queryset(
            BlogPage.objects.live().public().filter(authors__author__person_page=self.id).order_by('-date'),
            info, **kwargs
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
        FieldPanel('short_intro', classname="full"),
        FieldPanel('alt_short_intro', classname="full"),
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

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLString('first_name'),
        GraphQLString('last_name'),
        GraphQLString('role'),
        GraphQLBoolean('is_senior'),
        GraphQLString('short_intro'),
        GraphQLString('alt_short_intro'),
        GraphQLString('intro'),
        GraphQLString('biography'),
        GraphQLString('short_biography'),
        GraphQLImage('image'),
        GraphQLImage('feed_image'),
        GraphQLCollection(
            GraphQLForeignKey,
            'blog_posts',
            'blog.BlogPage'
        ),
    ]


# Person index
class PersonIndexPage(TorchboxPage):
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

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLString('strapline')
    ]


class CulturePageLink(Orderable):
    page = ParentalKey('people.CulturePage', related_name='links')
    title = models.TextField()
    description = models.TextField()
    link = models.ForeignKey('wagtailcore.Page', on_delete=models.CASCADE, blank=True, null=True)

    panels = [
        FieldPanel('title', classname="full"),
        FieldPanel('description', classname="full"),
        PageChooserPanel('link')
    ]

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('description'),
        GraphQLString('title'),
        GraphQLPage('link'),
    ]


class CulturePage(TorchboxPage):
    strapline = models.TextField()
    strapline_visible = models.BooleanField(
        help_text='Hide strapline visually but leave it readable by screen '
                  'readers.'
    )
    hero_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = RichTextField(blank=True)
    body = StreamField(StoryBlock())
    contact = models.ForeignKey('people.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('strapline', classname="full"),
        FieldPanel('strapline_visible'),
        ImageChooserPanel('hero_image'),
        FieldPanel('intro', classname="full"),
        InlinePanel('links', label='Link'),
        StreamFieldPanel('body'),
        SnippetChooserPanel('contact'),
    ]

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLString('strapline'),
        GraphQLString('strapline_visible'),
        GraphQLImage('hero_image'),
        GraphQLString('intro'),
        GraphQLStreamfield('body'),
        GraphQLCollection(
            GraphQLForeignKey,
            'links',
            'people.culturepagelink'
        ),
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

    @property
    def url(self):
        if self.person_page:
            return self.person_page.url
        return None

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

    graphql_fields = [
        GraphQLString('name'),
        GraphQLString('role'),
        GraphQLImage('image'),
        GraphQLString('url'),
        GraphQLForeignKey('person_page', 'people.PersonPage')
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
    default_contact = models.BooleanField(default=False, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField('name'),
    ]

    @property
    def contact_number(self):
        return self.phone_number.raw_input

    panels = [
        FieldPanel('name'),
        FieldPanel('role'),
        FieldPanel('default_contact', widget=forms.CheckboxInput),
        ImageChooserPanel('image'),
        FieldPanel('email_address'),
        FieldPanel('phone_number'),
    ]

    graphql_fields = [
        GraphQLString('name'),
        GraphQLString('role'),
        GraphQLImage('image'),
        GraphQLString('email_address'),
        GraphQLString('number', source='contact_number'),
        GraphQLBoolean('default_contact'),
    ]


class ContactReason(Orderable):
    page = ParentalKey('people.ContactReasonsList', related_name='reasons')
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('description'),
    ]


@register_snippet
class ContactReasonsList(ClusterableModel):
    name = models.CharField(max_length=255, blank=True)
    heading = models.TextField(blank=False)
    is_default = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('heading'),
        FieldPanel('is_default', widget=forms.CheckboxInput),
        InlinePanel('reasons', label='Reasons', max_num=3)
    ]

    graphql_fields = [
        GraphQLString('name'),
        GraphQLString('heading'),
        GraphQLBoolean('is_default'),
        GraphQLCollection(
            GraphQLForeignKey,
            'reasons',
            ContactReason
        )
    ]

    def clean(self):
        if self.is_default:
            qs = ContactReasonsList.objects.filter(is_default=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({
                    'is_default': [
                        'There already is another default snippet.',
                    ],
                })
