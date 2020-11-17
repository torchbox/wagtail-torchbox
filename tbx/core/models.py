from django import forms
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.admin.mail import send_mail
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.blocks import PageChooserBlock, StreamBlock, StructBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.search import index
from wagtail.snippets.models import register_snippet

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
        PageChooserPanel("link_page"),
        DocumentChooserPanel("link_document"),
    ]

    class Meta:
        abstract = True


# Carousel items
class CarouselItem(LinkFields):
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel("image"),
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
        PageChooserPanel("page"),
        FieldPanel("url"),
        FieldPanel("text"),
    ]

    def __str__(self):
        return self.text


register_snippet(Advert)


# Custom image
class TorchboxImage(AbstractImage):
    credit = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + ("credit",)

    @property
    def credit_text(self):
        return self.credit


class TorchboxRendition(AbstractRendition):
    image = models.ForeignKey(
        "TorchboxImage", on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


# Home Page


class HomePageHero(Orderable, RelatedLink):
    page = ParentalKey("torchbox.HomePage", related_name="hero")
    colour = models.CharField(
        max_length=255,
        help_text="Hex ref colour of link and background gradient, use #23b0b0 for default blue",
    )
    background = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    logo = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    text = models.CharField(max_length=255)

    panels = RelatedLink.panels + [
        ImageChooserPanel("background"),
        ImageChooserPanel("logo"),
        FieldPanel("colour"),
        FieldPanel("text"),
    ]


class HomePageClient(Orderable, RelatedLink):
    page = ParentalKey("torchbox.HomePage", related_name="clients")
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = RelatedLink.panels + [ImageChooserPanel("image")]


class HomePage(Page):
    hero_intro_primary = models.TextField(blank=True)
    hero_intro_secondary = models.TextField(blank=True)
    intro_body = RichTextField(blank=True)
    work_title = models.TextField(blank=True)
    blog_title = models.TextField(blank=True)
    clients_title = models.TextField(blank=True)

    class Meta:
        verbose_name = "Homepage"

    content_panels = [
        FieldPanel("title", classname="full title"),
        MultiFieldPanel(
            [FieldPanel("hero_intro_primary"), FieldPanel("hero_intro_secondary")],
            heading="Hero intro",
        ),
        InlinePanel("hero", label="Hero"),
        FieldPanel("intro_body"),
        FieldPanel("work_title"),
        FieldPanel("blog_title"),
        FieldPanel("clients_title"),
        InlinePanel("clients", label="Clients"),
    ]

    @property
    def blog_posts(self):
        from tbx.blog.models import BlogPage

        # Get list of blog pages.
        blog_posts = BlogPage.objects.live().public()

        # Order by most recent date first
        blog_posts = blog_posts.order_by("-date")

        return blog_posts


# Standard page


class StandardPage(Page):
    template = "patterns/pages/standard/standard_page.html"

    body = StreamField(StoryBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
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


class JobIndexPage(Page):
    strapline = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    jobs_xml_feed = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("strapline", classname="full title"),
        FieldPanel("intro"),
        FieldPanel("jobs_xml_feed"),
    ]


class GoogleAdGrantApplication(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        ordering = ["-date"]


class GoogleAdGrantApplicationForm(forms.ModelForm):
    class Meta:
        model = GoogleAdGrantApplication
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your charity's name"}),
            "email": forms.TextInput(attrs={"placeholder": "Your email address"}),
        }


class GoogleAdGrantsPageGrantsManaged(models.Model):
    page = ParentalKey("torchbox.GoogleAdGrantsPage", related_name="grants_managed")
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [ImageChooserPanel("image")]


class GoogleAdGrantsPageQuote(Orderable):
    page = ParentalKey("torchbox.GoogleAdGrantsPage", related_name="quotes")
    text = models.TextField()
    person_name = models.CharField(max_length=255)
    organisation_name = models.CharField(max_length=255)

    panels = [
        FieldPanel("text"),
        FieldPanel("person_name"),
        FieldPanel("organisation_name"),
    ]


class GoogleAdGrantsAccreditations(Orderable):
    page = ParentalKey("torchbox.GoogleAdGrantsPage", related_name="accreditations")
    image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [ImageChooserPanel("image")]


class GoogleAdGrantsPage(Page):
    intro = RichTextField()
    form_title = models.CharField(max_length=255)
    form_subtitle = models.CharField(max_length=255)
    form_button_text = models.CharField(max_length=255)
    to_address = models.EmailField(
        verbose_name="to address",
        blank=True,
        help_text="Optional - form submissions will be emailed to this address",
    )
    body = RichTextField()
    grants_managed_title = models.CharField(max_length=255)
    call_to_action_title = models.CharField(max_length=255, blank=True)
    call_to_action_embed_url = models.URLField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        form = GoogleAdGrantApplicationForm()
        context = super(GoogleAdGrantsPage, self).get_context(request, *args, **kwargs)
        context["form"] = form
        return context

    def serve(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            form = GoogleAdGrantApplicationForm(request.POST)
            if form.is_valid():
                form.save()

                if self.to_address:
                    subject = "{} form submission".format(self.title)
                    content = "\n".join(
                        [
                            x[1].label + ": " + str(form.data.get(x[0]))
                            for x in form.fields.items()
                        ]
                    )
                    send_mail(
                        subject, content, [self.to_address],
                    )
                return render(
                    request,
                    "torchbox/includes/ad_grant_application_landing.html",
                    {"self": self, "form": form},
                )
            else:
                return render(
                    request,
                    "torchbox/includes/ad_grant_application_form.html",
                    {"self": self, "form": form},
                )
        else:
            return super(GoogleAdGrantsPage, self).serve(request)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
        FieldPanel("body", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("form_title"),
                FieldPanel("form_subtitle"),
                FieldPanel("form_button_text"),
                FieldPanel("to_address"),
            ],
            "Application Form",
        ),
        MultiFieldPanel(
            [
                FieldPanel("grants_managed_title"),
                InlinePanel("grants_managed", label="Grants Managed"),
            ],
            "Grants Managed Section",
        ),
        InlinePanel("quotes", label="Quotes"),
        MultiFieldPanel(
            [
                FieldPanel("call_to_action_title"),
                FieldPanel("call_to_action_embed_url"),
                InlinePanel("accreditations", label="Accreditations"),
            ],
            "Call To Action",
        ),
    ]


@register_setting
class GlobalSettings(BaseSetting):
    contact_telephone = models.CharField(max_length=255, help_text="Telephone")
    contact_email = models.EmailField(max_length=255, help_text="Email address")
    contact_twitter = models.CharField(max_length=255, help_text="Twitter")
    email_newsletter_teaser = models.CharField(
        max_length=255, help_text="Text that sits above the email newsletter"
    )
    oxford_address_title = models.CharField(max_length=255, help_text="Full address")
    oxford_address = RichTextField(help_text="Full address")
    oxford_address_link = models.URLField(
        max_length=255, help_text="Link to google maps"
    )
    oxford_address_svg = models.CharField(
        max_length=9000, help_text="Paste SVG code here"
    )
    bristol_address_title = models.CharField(max_length=255, help_text="Full address")
    bristol_address = RichTextField(help_text="Full address")
    bristol_address_link = models.URLField(
        max_length=255, help_text="Link to google maps"
    )
    bristol_address_svg = models.CharField(
        max_length=9000, help_text="Paste SVG code here"
    )
    us_address_title = models.CharField(max_length=255, help_text="Full address")
    us_address = RichTextField(help_text="Full address")
    us_address_link = models.URLField(max_length=255, help_text="Link to google maps")
    us_address_svg = models.CharField(max_length=9000, help_text="Paste SVG code here")
    us_address_title = models.CharField(max_length=255, help_text="Full address")
    cambridge_address = RichTextField(help_text="Full address", blank=True)
    cambridge_address_link = models.URLField(
        max_length=255, help_text="Link to google maps", blank=True
    )
    cambridge_address_svg = models.CharField(
        max_length=9000, help_text="Paste SVG code here", blank=True
    )
    cambridge_address_title = models.CharField(
        max_length=255, help_text="Full address", blank=True
    )

    # Contact widget
    contact_person = models.ForeignKey(
        "people.PersonPage",
        related_name="+",
        null=True,
        on_delete=models.SET_NULL,
        help_text="Ensure this person has telephone and email fields set",
    )
    contact_widget_intro = models.TextField()
    contact_widget_call_to_action = models.TextField()
    contact_widget_button_text = models.TextField()

    class Meta:
        verbose_name = "Global Settings"

    panels = [
        FieldPanel("contact_telephone"),
        FieldPanel("contact_email"),
        FieldPanel("contact_twitter"),
        FieldPanel("email_newsletter_teaser"),
        FieldPanel("oxford_address_title"),
        FieldPanel("oxford_address"),
        FieldPanel("oxford_address_link"),
        FieldPanel("oxford_address_svg"),
        FieldPanel("bristol_address_title"),
        FieldPanel("bristol_address"),
        FieldPanel("bristol_address_link"),
        FieldPanel("bristol_address_svg"),
        FieldPanel("us_address_title"),
        FieldPanel("us_address"),
        FieldPanel("us_address_link"),
        FieldPanel("us_address_svg"),
        FieldPanel("cambridge_address_title"),
        FieldPanel("cambridge_address"),
        FieldPanel("cambridge_address_link"),
        FieldPanel("cambridge_address_svg"),
        MultiFieldPanel(
            [
                PageChooserPanel("contact_person"),
                FieldPanel("contact_widget_intro"),
                FieldPanel("contact_widget_call_to_action"),
                FieldPanel("contact_widget_button_text"),
            ],
            "Contact widget",
        ),
    ]


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
class MainMenu(BaseSetting):
    menu = StreamField(MenuBlock(), blank=True)

    panels = [
        StreamFieldPanel("menu"),
    ]
