from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from tbx.core.blocks import PageSectionStoryBlock
from tbx.core.utils.models import SocialFields
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.blocks import PageChooserBlock, StreamBlock, StructBlock
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet

from .api import PeopleHRFeed
from .blocks import StoryBlock
from .fields import ColorField


# A couple of abstract classes that contain commonly used fields
class ContentBlock(models.Model):
    content = RichTextField()

    panels = [
        FieldPanel("content"),
    ]

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    link_document = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel("link_external"),
        FieldPanel("link_page"),
        FieldPanel("link_document"),
    ]

    class Meta:
        abstract = True


# Carousel items
class CarouselItem(LinkFields):
    image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("embed_url"),
        FieldPanel("caption"),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel("title"),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Advert Snippet
class AdvertPlacement(models.Model):
    page = ParentalKey("wagtailcore.Page", related_name="advert_placements")
    advert = models.ForeignKey(
        "torchbox.Advert", on_delete=models.CASCADE, related_name="+"
    )


class Advert(models.Model):
    page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="adverts",
    )
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel("page"),
        FieldPanel("url"),
        FieldPanel("text"),
    ]

    def __str__(self):
        return self.text


register_snippet(Advert)


# Home Page


class HomePageFeaturedPost(Orderable):
    page = ParentalKey(
        "torchbox.HomePage", on_delete=models.CASCADE, related_name="featured_posts"
    )
    featured_post = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        PageChooserPanel("featured_post", ["blog.BlogPage", "work.WorkPage"]),
    ]


class HomePageHeroImage(Orderable):
    page = ParentalKey(
        "torchbox.HomePage", on_delete=models.CASCADE, related_name="hero_images"
    )
    image = models.ForeignKey(
        "images.CustomImage",
        help_text="The hero images will be displayed in a random order.",
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="+",
    )


class HomePage(SocialFields, Page):
    template = "patterns/pages/home/home_page.html"
    hero_intro_primary = models.TextField(blank=True)
    hero_intro_secondary = models.TextField(blank=True)
    intro_body = RichTextField(blank=True)
    work_title = models.TextField(blank=True)
    blog_title = models.TextField(blank=True)
    clients_title = models.TextField(blank=True)

    class Meta:
        verbose_name = "Homepage"

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_intro_primary"),
                FieldPanel("hero_intro_secondary"),
                InlinePanel("hero_images", label="Hero Images", max_num=6, min_num=1),
            ],
            heading="Hero intro",
        ),
        InlinePanel("featured_posts", label="Featured Posts", max_num=3),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            hero_images=self.hero_images.all(),
        )
        return context

    @property
    def blog_posts(self):
        from tbx.blog.models import BlogPage

        # Get list of blog pages.
        blog_posts = BlogPage.objects.live().public()

        # Order by most recent date first
        blog_posts = blog_posts.order_by("-date")

        return blog_posts


# Standard page


class StandardPage(SocialFields, Page):
    template = "patterns/pages/standard/standard_page.html"

    body = StreamField(StoryBlock(), use_json_field=True)
    additional_content = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
        verbose_name="Call to action",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("additional_content"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]


@register_snippet
class ParticleSnippet(models.Model):
    """
    Snippet for configuring particlejs options
    """

    # particle type choices
    CIRCLE = 1
    EDGE = 2
    TRIANGLE = 3
    POLYGON = 4
    STAR = 5
    IMAGE = 6
    PARTICLES_TYPE_CHOICES = (
        (CIRCLE, "circle"),
        (EDGE, "edge"),
        (TRIANGLE, "triangle"),
        (POLYGON, "polygon"),
        (STAR, "star"),
        (IMAGE, "image"),
    )
    # particle movement direction choices
    NONE = 1
    TOP = 2
    TOP_RIGHT = 3
    RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6
    BOTTOM_LEFT = 7
    LEFT = 8
    PARTICLES_MOVE_DIRECTION_CHOICES = (
        (NONE, "none"),
        (TOP, "top"),
        (TOP_RIGHT, "top-right"),
        (RIGHT, "right"),
        (BOTTOM_RIGHT, "bottom-right"),
        (BOTTOM, "bottom"),
        (BOTTOM_LEFT, "bottom-left"),
        (LEFT, "left"),
    )
    title = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField(default=50)
    shape_type = models.PositiveSmallIntegerField(
        choices=PARTICLES_TYPE_CHOICES, default=CIRCLE
    )
    polygon_sides = models.PositiveSmallIntegerField(default=5)
    size = models.DecimalField(default=2.5, max_digits=4, decimal_places=1)
    size_random = models.BooleanField(default=False)
    colour = ColorField(default="ffffff", help_text="Don't include # symbol.")
    opacity = models.DecimalField(default=0.9, max_digits=2, decimal_places=1)
    opacity_random = models.BooleanField(default=False)
    move_speed = models.DecimalField(default=2.5, max_digits=2, decimal_places=1)
    move_direction = models.PositiveSmallIntegerField(
        choices=PARTICLES_MOVE_DIRECTION_CHOICES, default=NONE
    )
    line_linked = models.BooleanField(default=True)
    css_background_colour = ColorField(
        blank=True,
        help_text="Don't include # symbol. Will be overridden by linear gradient",
    )
    css_background_linear_gradient = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter in the format 'to right, #2b2b2b 0%, #243e3f 28%, #2b2b2b 100%'",
    )
    css_background_url = models.URLField(blank=True, max_length=255)

    def __str__(self):
        return self.title


# Currently hidden. These were used in the past and may be used again in the future
# @register_snippet
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Jobs index page

# NOTE: This block has been retired due to the jobs page now being fed via PeopleHR API
class JobIndexPageJob(Orderable):
    page = ParentalKey("torchbox.JobIndexPage", related_name="jobs")
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    url = models.URLField(null=True)
    location = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("level"),
        FieldPanel("url"),
        FieldPanel("location"),
    ]


class JobIndexPage(SocialFields, Page):
    template = "patterns/pages/job/job_listing.html"

    strapline = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    jobs_xml_feed = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("strapline", classname="title"),
        FieldPanel("intro"),
        FieldPanel("jobs_xml_feed"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
    ]

    def serve(self, request):
        try:
            feed = PeopleHRFeed()
            jobs = feed.get_jobs(url=self.jobs_xml_feed)
        except Exception as e:
            jobs = []
            raise e

        return render(
            request,
            self.template,
            {"page": self, "jobs": jobs, "feed_success": len(jobs) > 0},
        )

    def serve_preview(self, request, mode_name):
        return self.serve(request)


class BaseAddress(blocks.StructBlock):
    title = blocks.CharBlock(blank=True)
    address = blocks.RichTextBlock(blank=True)


@register_setting
class GlobalSettings(BaseSiteSetting):
    addresses = StreamField(
        [("address", BaseAddress())], blank=True, use_json_field=True
    )

    panels = [
        FieldPanel("addresses"),
    ]

    class Meta:
        verbose_name = "Global Settings"


class SubMenuItemBlock(StreamBlock):
    # subitem = PageChooserBlock()
    related_listing_page = PageChooserBlock()


class MenuItemBlock(StructBlock):
    page = PageChooserBlock()
    subitems = SubMenuItemBlock(blank=True, null=True)

    class Meta:
        template = "torchbox/includes/menu_item.html"


class MenuBlock(StreamBlock):
    items = MenuItemBlock()


@register_setting
class MainMenu(BaseSiteSetting):
    menu = StreamField(MenuBlock(), blank=True, use_json_field=True)

    panels = [
        FieldPanel("menu"),
    ]
