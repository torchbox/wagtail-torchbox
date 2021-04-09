from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock

from tbx.blog.models import BlogPage
from tbx.core.blocks import StoryBlock
from tbx.people.forms import ContactForm


class PersonPage(Page):
    template = "patterns/pages/team/team_detail.html"

    parent_page_types = ["PersonIndexPage"]

    role = models.CharField(max_length=255, blank=True)
    is_senior = models.BooleanField(default=False)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("biography"),
    ]

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("role"),
        FieldPanel("is_senior"),
        FieldPanel("intro", classname="full"),
        FieldPanel("biography", classname="full"),
        ImageChooserPanel("image"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    @cached_property
    def author_blogs(self):
        # return the blogs writen by this member
        author_snippet = Author.objects.get(person_page__pk=self.pk)
        return BlogPage.objects.filter(authors__author=author_snippet).order_by("-date")


# Person index
class PersonIndexPage(Page):
    strapline = models.CharField(max_length=255)
    template = "patterns/pages/team/team_listing.html"

    subpage_types = ["PersonPage"]

    @cached_property
    def team(self):
        return PersonPage.objects.order_by("-is_senior", "title").live().public()

    content_panels = Page.content_panels + [
        FieldPanel("strapline", classname="full"),
    ]


class CulturePageLink(Orderable):
    page = ParentalKey("people.CulturePage", related_name="links")
    title = models.TextField()
    description = models.TextField()
    link = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, blank=True, null=True
    )

    panels = [
        FieldPanel("title", classname="full"),
        FieldPanel("description", classname="full"),
        PageChooserPanel("link"),
    ]


class CulturePage(Page):
    template = "patterns/pages/culture/culture_page.html"

    strapline = models.TextField()
    strapline_visible = models.BooleanField(
        help_text="Hide strapline visually but leave it readable by screen " "readers."
    )
    hero_image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = RichTextField(blank=True)
    body = StreamField(StoryBlock())
    contact = models.ForeignKey(
        "people.Contact",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("strapline", classname="full"),
        FieldPanel("strapline_visible"),
        ImageChooserPanel("hero_image"),
        FieldPanel("intro", classname="full"),
        InlinePanel("links", label="Link"),
        StreamFieldPanel("body"),
        SnippetChooserPanel("contact"),
    ]


class ValuesPage(Page):
    template = "patterns/pages/values/values_page.html"

    strapline = models.TextField()
    intro = RichTextField(blank=True)

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("strapline", classname="full"),
        FieldPanel("intro", classname="full"),
        MultiFieldPanel(
            [
                InlinePanel("values", label="Values"),
            ],
            heading="Values",
        ),
    ]


class BaseValuesPageValue(models.Model):
    value_image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    text = RichTextField(blank=True)
    heading = models.CharField(max_length=255)
    panels = [
        ImageChooserPanel("value_image"),
        FieldPanel("heading"),
        FieldPanel("text"),
    ]

    class Meta:
        abstract = True


class ValuesPageValue(Orderable, BaseValuesPageValue):
    page = ParentalKey(ValuesPage, related_name="values")


# An author snippet which keeps a copy of a person's details in case they leave and their page is unpublished
# Could also be used for external authors
@register_snippet
class Author(index.Indexed, models.Model):
    person_page = models.OneToOneField(
        "people.PersonPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def update_manual_fields(self, person_page):
        self.name = person_page.title
        self.role = person_page.role
        self.image = person_page.image

    def clean(self):
        if not self.person_page and not self.name:
            raise ValidationError(
                {"person_page": "You must set either 'Person page' or 'Name'"}
            )

        if self.person_page:
            self.update_manual_fields(self.person_page)

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField("name"),
    ]

    panels = [
        PageChooserPanel("person_page"),
        MultiFieldPanel(
            [FieldPanel("name"), FieldPanel("role"), ImageChooserPanel("image")],
            "Manual fields",
        ),
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
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    email_address = models.EmailField()
    phone_number = PhoneNumberField()
    default_contact = models.BooleanField(default=False, blank=True, null=True)
    base_form_class = ContactForm

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField("name"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("default_contact", widget=forms.CheckboxInput),
        ImageChooserPanel("image"),
        FieldPanel("email_address"),
        FieldPanel("phone_number"),
    ]


class ContactReason(Orderable):
    page = ParentalKey("people.ContactReasonsList", related_name="reasons")
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)


@register_snippet
class ContactReasonsList(ClusterableModel):
    name = models.CharField(max_length=255, blank=True)
    heading = models.TextField(blank=False)
    is_default = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("heading"),
        FieldPanel("is_default", widget=forms.CheckboxInput),
        InlinePanel("reasons", label="Reasons", max_num=3),
    ]

    def clean(self):
        if self.is_default:
            qs = ContactReasonsList.objects.filter(is_default=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    {"is_default": ["There already is another default snippet."]}
                )
