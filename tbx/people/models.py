from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from phonenumber_field.modelfields import PhoneNumberField
from tbx.blog.models import BlogIndexPage, BlogPage
from tbx.core.blocks import PageSectionStoryBlock
from tbx.core.utils.models import SocialFields
from tbx.people.blocks import InstagramEmbedBlock, StandoutItemsBlock
from tbx.people.forms import ContactForm
from tbx.work.models import WorkIndexPage, WorkPage
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.signals import page_published
from wagtail.snippets.models import register_snippet


class PersonPage(SocialFields, Page):
    template = "patterns/pages/team/team_detail.html"

    parent_page_types = ["PersonIndexPage"]

    role = models.CharField(max_length=255, blank=True)
    is_senior = models.BooleanField(default=False)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("biography"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("role"),
        FieldPanel("is_senior"),
        FieldPanel("intro"),
        FieldPanel("biography"),
        FieldPanel("image"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    @cached_property
    def author_posts(self):
        # return the blogs writen by this member
        author_snippet = Author.objects.get(person_page__pk=self.pk)

        # format for template
        return [
            {
                "title": blog_post.title,
                "url": blog_post.url,
                "author": blog_post.first_author,
                "date": blog_post.date,
            }
            for blog_post in BlogPage.objects.live()
            .filter(authors__author=author_snippet)
            .order_by("-date")
        ]

    @cached_property
    def related_works(self):
        # Get the latest 2 work pages by this author
        works = (
            WorkPage.objects.filter(authors__author__person_page=self.pk)
            .live()
            .public()
            .distinct()
            .order_by("-date")[:2]
        )
        return works

    @cached_property
    def work_index(self):
        return WorkIndexPage.objects.live().public().first()


# Person index
class PersonIndexPage(SocialFields, Page):
    strapline = models.CharField(max_length=255)
    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
    )

    template = "patterns/pages/team/team_listing.html"

    subpage_types = ["PersonPage"]

    @cached_property
    def team(self):
        return PersonPage.objects.order_by("-is_senior", "title").live().public()

    content_panels = Page.content_panels + [
        FieldPanel("strapline"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]


class CulturePageLink(Orderable):
    page = ParentalKey("people.CulturePage", related_name="links")
    title = models.TextField()
    description = models.TextField()
    link = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, blank=True, null=True
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("link"),
    ]


# Was previously the culture page until it was re-purposed to be the careers page
class CulturePage(SocialFields, Page):
    template = "patterns/pages/careers/careers_page.html"

    strapline = models.TextField()
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = RichTextField(blank=True)
    benefits_heading = RichTextField(blank=True)
    benefits_section_title = models.TextField(blank=True, default="Benefits")
    standout_items = StreamField(
        [("item", StandoutItemsBlock())], blank=True, use_json_field=True
    )

    blogs_section_title = models.CharField(
        blank=True,
        max_length=100,
        verbose_name="Title",
    )
    featured_blog_posts = StreamField(
        [("blog_post", blocks.PageChooserBlock(page_type="blog.BlogPage"))],
        blank=True,
        verbose_name="Blog posts",
        use_json_field=True,
    )

    instagram_posts = StreamField(
        [("post", InstagramEmbedBlock())],
        blank=True,
        null=True,
        min_num=8,
        max_num=8,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("strapline"),
        FieldPanel("hero_image"),
        FieldPanel("intro"),
        InlinePanel("links", label="Link"),
        MultiFieldPanel(
            [
                FieldPanel("benefits_section_title"),
                FieldPanel("benefits_heading"),
                InlinePanel("key_benefits", label="Key benefits", max_num=10),
            ],
            heading="Key Benefits",
            classname="collapsible",
        ),
        FieldPanel("standout_items"),
        MultiFieldPanel(
            [FieldPanel("blogs_section_title"), FieldPanel("featured_blog_posts")],
            heading="Featured Blog Posts",
            classname="collapsible",
        ),
        FieldPanel("instagram_posts"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    class Meta:
        verbose_name = "Careers Page"

    def get_standout_items(self):
        """Format the standout items data for the template."""
        return [
            {
                "title": standout_item.value["title"],
                "subtitle": standout_item.value["subtitle"],
                "description": standout_item.value["description"],
                "url": standout_item.block.get_link(
                    standout_item.value["link"],
                ),
                "image": standout_item.value["image"],
            }
            for standout_item in self.standout_items
        ]

    def get_featured_blog_posts(self):
        """Format the featured blog posts for the template."""

        return [
            {
                "title": blog_post.value.title,
                "url": blog_post.value.url,
                "author": blog_post.value.first_author,
                "date": blog_post.value.date,
            }
            for blog_post in self.featured_blog_posts
            if blog_post.value.live
        ]

    def get_context(self, request):
        context = super().get_context(request)
        context["standout_items"] = self.get_standout_items()
        context.update(
            featured_blog_posts=self.get_featured_blog_posts(),
            blog_index_page=BlogIndexPage.objects.live().first(),
        )
        return context

    @property
    def filter_by(self):
        return "culture"


class BaseCulturePageKeyPoint(models.Model):
    text = models.CharField(max_length=255)
    linked_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    panels = [
        FieldPanel("text"),
        FieldPanel("linked_page"),
    ]

    class Meta:
        abstract = True


class CulturePageKeyPoint(Orderable, BaseCulturePageKeyPoint):
    page = ParentalKey(CulturePage, related_name="key_benefits")


class ValuesPage(SocialFields, Page):
    template = "patterns/pages/values/values_page.html"

    strapline = models.TextField()
    intro = RichTextField(blank=True)
    standout_items = StreamField(
        [("item", StandoutItemsBlock())], blank=True, use_json_field=True
    )
    blogs_section_title = models.CharField(
        blank=True, max_length=100, verbose_name="Title"
    )
    featured_blog_posts = StreamField(
        [("blog_post", blocks.PageChooserBlock(page_type="blog.BlogPage"))],
        blank=True,
        verbose_name="Blog posts",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("strapline"),
        FieldPanel("intro"),
        InlinePanel("values", heading="Values", label="Values"),
        FieldPanel("standout_items"),
        MultiFieldPanel(
            [FieldPanel("blogs_section_title"), FieldPanel("featured_blog_posts")],
            heading="Featured Blog Posts",
            classname="collapsible",
        ),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    class Meta:
        verbose_name = "Values Page"

    def get_standout_items(self):
        """Format the standout items data for the template."""
        return [
            {
                "title": standout_item.value["title"],
                "subtitle": standout_item.value["subtitle"],
                "description": standout_item.value["description"],
                "url": standout_item.block.get_link(standout_item.value["link"]),
                "image": standout_item.value["image"],
            }
            for standout_item in self.standout_items
        ]

    def get_featured_blog_posts(self):
        """Format the featured blog posts for the template."""
        return [
            {
                "title": blog_post.value.title,
                "url": blog_post.value.url,
                "author": blog_post.value.first_author,
                "date": blog_post.value.date,
            }
            for blog_post in self.featured_blog_posts
            if blog_post.value.live
        ]

    def get_context(self, request):
        context = super().get_context(request)
        context["standout_items"] = self.get_standout_items()
        context.update(
            featured_blog_posts=self.get_featured_blog_posts(),
            blog_index_page=BlogIndexPage.objects.live().first(),
        )
        return context


class BaseValuesPageValue(models.Model):
    value_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    text = RichTextField(blank=True)
    heading = models.CharField(max_length=255)
    panels = [
        FieldPanel("value_image"),
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
        "images.CustomImage",
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
        index.AutocompleteField("name"),
        index.SearchField("name"),
    ]

    panels = [
        FieldPanel("person_page"),
        MultiFieldPanel(
            [FieldPanel("name"), FieldPanel("role"), FieldPanel("image")],
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
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    email_address = models.EmailField()
    phone_number = PhoneNumberField(blank=True, null=True)
    default_contact = models.BooleanField(default=False, blank=True, null=True)
    base_form_class = ContactForm

    def __str__(self):
        return self.name

    search_fields = [
        index.AutocompleteField("name"),
        index.SearchField("name"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("default_contact", widget=forms.CheckboxInput),
        FieldPanel("image"),
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
