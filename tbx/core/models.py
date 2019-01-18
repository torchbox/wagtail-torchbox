from django import forms
from django.db import models
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.admin.utils import send_mail
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.blocks import PageChooserBlock, StreamBlock, StructBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtailcaptcha.models import WagtailCaptchaEmailForm

from .blocks import StoryBlock
from .fields import ColorField


# A couple of abstract classes that contain commonly used fields
class ContentBlock(models.Model):
    content = RichTextField()

    panels = [
        FieldPanel('content'),
    ]

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
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
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


# Carousel items
class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Advert Snippet
class AdvertPlacement(models.Model):
    page = ParentalKey('wagtailcore.Page', related_name='advert_placements')
    advert = models.ForeignKey('torchbox.Advert', related_name='+')


class Advert(models.Model):
    page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='adverts',
        null=True,
        blank=True
    )
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text


register_snippet(Advert)


# Custom image
class TorchboxImage(AbstractImage):
    credit = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'credit',
    )

    @property
    def credit_text(self):
        return self.credit


class TorchboxRendition(AbstractRendition):
    image = models.ForeignKey('TorchboxImage', related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Home Page

class HomePageHero(Orderable, RelatedLink):
    page = ParentalKey('torchbox.HomePage', related_name='hero')
    colour = models.CharField(max_length=255, help_text="Hex ref colour of link and background gradient, use #23b0b0 for default blue")
    background = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    logo = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text = models.CharField(
        max_length=255
    )

    panels = RelatedLink.panels + [
        ImageChooserPanel('background'),
        ImageChooserPanel('logo'),
        FieldPanel('colour'),
        FieldPanel('text'),
    ]


class HomePageClient(Orderable, RelatedLink):
    page = ParentalKey('torchbox.HomePage', related_name='clients')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = RelatedLink.panels + [
        ImageChooserPanel('image')
    ]


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
        FieldPanel('title', classname="full title"),
        MultiFieldPanel(
            [
                FieldPanel('hero_intro_primary'),
                FieldPanel('hero_intro_secondary'),
            ],
            heading="Hero intro"
        ),
        InlinePanel('hero', label="Hero"),
        FieldPanel('intro_body'),
        FieldPanel('work_title'),
        FieldPanel('blog_title'),
        FieldPanel('clients_title'),
        InlinePanel('clients', label="Clients"),
    ]

    @property
    def blog_posts(self):
        from tbx.blog.models import BlogPage

        # Get list of blog pages.
        blog_posts = BlogPage.objects.live().public()

        # Order by most recent date first
        blog_posts = blog_posts.order_by('-date')

        return blog_posts


# Standard page

class StandardPageContentBlock(Orderable, ContentBlock):
    page = ParentalKey('torchbox.StandardPage', related_name='content_block')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.StandardPage', related_name='related_links')


class StandardPageClient(Orderable, RelatedLink):
    page = ParentalKey('torchbox.StandardPage', related_name='clients')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = RelatedLink.panels + [
        ImageChooserPanel('image')
    ]


class StandardPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    credit = models.CharField(max_length=255, blank=True)
    heading = RichTextField(blank=True)
    quote = models.CharField(max_length=255, blank=True)
    intro = RichTextField("Intro (deprecated. Use streamfield instead)", blank=True)
    middle_break = RichTextField(blank=True)
    body = RichTextField("Body (deprecated. Use streamfield instead)", blank=True)
    streamfield = StreamField(StoryBlock())
    email = models.EmailField(blank=True)

    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    show_in_play_menu = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        ImageChooserPanel('main_image'),
        FieldPanel('credit', classname="full"),
        FieldPanel('heading', classname="full"),
        FieldPanel('quote', classname="full"),
        FieldPanel('intro', classname="full"),
        FieldPanel('middle_break', classname="full"),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('streamfield'),
        FieldPanel('email', classname="full"),
        InlinePanel('content_block', label="Content block"),
        InlinePanel('related_links', label="Related links"),
        InlinePanel('clients', label="Clients"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('show_in_play_menu'),
        ImageChooserPanel('feed_image'),
    ]


# About page
class AboutPageRelatedLinkButton(Orderable, RelatedLink):
    page = ParentalKey('torchbox.AboutPage', related_name='related_link_buttons')


class AboutPageOffice(Orderable):
    page = ParentalKey('torchbox.AboutPage', related_name='offices')
    title = models.TextField()
    svg = models.TextField(null=True)
    description = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('svg')
    ]


class AboutPageContentBlock(Orderable):
    page = ParentalKey('torchbox.AboutPage', related_name='content_blocks')
    year = models.IntegerField()
    title = models.TextField()
    description = models.TextField()
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('year'),
        FieldPanel('title'),
        FieldPanel('description'),
        ImageChooserPanel('image')
    ]


class AboutPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    involvement_title = models.TextField(blank=True)

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        FieldPanel('heading', classname='full'),
        FieldPanel('intro', classname='full'),
        InlinePanel('related_link_buttons', label='Header buttons'),
        InlinePanel('content_blocks', label='Content blocks'),
        InlinePanel('offices', label='Offices'),
        FieldPanel('involvement_title'),
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
        (CIRCLE, 'circle'),
        (EDGE, 'edge'),
        (TRIANGLE, 'triangle'),
        (POLYGON, 'polygon'),
        (STAR, 'star'),
        (IMAGE, 'image'),
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
        (NONE, 'none'),
        (TOP, 'top'),
        (TOP_RIGHT, 'top-right'),
        (RIGHT, 'right'),
        (BOTTOM_RIGHT, 'bottom-right'),
        (BOTTOM, 'bottom'),
        (BOTTOM_LEFT, 'bottom-left'),
        (LEFT, 'left'),
    )
    title = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField(default=50)
    shape_type = models.PositiveSmallIntegerField(
        choices=PARTICLES_TYPE_CHOICES, default=CIRCLE)
    polygon_sides = models.PositiveSmallIntegerField(default=5)
    size = models.DecimalField(default=2.5, max_digits=4, decimal_places=1)
    size_random = models.BooleanField(default=False)
    colour = ColorField(default='ffffff', help_text="Don't include # symbol.")
    opacity = models.DecimalField(default=0.9, max_digits=2, decimal_places=1)
    opacity_random = models.BooleanField(default=False)
    move_speed = models.DecimalField(
        default=2.5, max_digits=2, decimal_places=1)
    move_direction = models.PositiveSmallIntegerField(
        choices=PARTICLES_MOVE_DIRECTION_CHOICES,
        default=NONE)
    line_linked = models.BooleanField(default=True)
    css_background_colour = ColorField(
        blank=True,
        help_text="Don't include # symbol. Will be overridden by linear gradient")
    css_background_linear_gradient = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter in the format 'to right, #2b2b2b 0%, #243e3f 28%, #2b2b2b 100%'")
    css_background_url = models.URLField(blank=True, max_length=255)

    def __str__(self):
        return self.title


@register_snippet
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Jobs index page
class ReasonToJoin(Orderable):
    page = ParentalKey('torchbox.JobIndexPage', related_name='reasons_to_join')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=511)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('body')
    ]


class JobIndexPageJob(Orderable):
    page = ParentalKey('torchbox.JobIndexPage', related_name='job')
    job_title = models.CharField(max_length=255)
    job_intro = models.CharField(max_length=255)
    url = models.URLField(null=True)
    location = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('job_title'),
        FieldPanel('job_intro'),
        FieldPanel("url"),
        FieldPanel("location"),
    ]


class JobIndexPage(Page):
    intro = models.TextField(blank=True)
    listing_intro = models.TextField(
        blank=True,
        help_text="Shown instead of the intro when job listings are included "
        "on other pages")
    no_jobs_that_fit = RichTextField(blank=True)
    terms_and_conditions = models.URLField(null=True)
    refer_a_friend = models.URLField(null=True)
    reasons_intro = models.TextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        from tbx.blog.models import BlogPage

        context = super(
            JobIndexPage, self
        ).get_context(request, *args, **kwargs)
        context['jobs'] = self.job.all()
        context['blogs'] = BlogPage.objects.live().order_by('-date')[:4]
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        FieldPanel('listing_intro', classname="full"),
        FieldPanel('no_jobs_that_fit', classname="full"),
        FieldPanel('terms_and_conditions', classname="full"),
        FieldPanel('refer_a_friend', classname="full"),
        InlinePanel('job', label="Job"),
        FieldPanel('reasons_intro', classname="full"),
        InlinePanel('reasons_to_join', label="Reasons To Join"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


class TshirtPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


TshirtPage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('main_image'),
]


class GoogleAdGrantApplication(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        ordering = ['-date']


class GoogleAdGrantApplicationForm(forms.ModelForm):
    class Meta:
        model = GoogleAdGrantApplication
        fields = [
            'name', 'email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Your charity's name"}),
            'email': forms.TextInput(attrs={'placeholder': "Your email address"})
        }


class GoogleAdGrantsPageGrantsManaged(models.Model):
    page = ParentalKey('torchbox.GoogleAdGrantsPage', related_name="grants_managed")
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]


class GoogleAdGrantsPageQuote(Orderable):
    page = ParentalKey('torchbox.GoogleAdGrantsPage', related_name="quotes")
    text = models.TextField()
    person_name = models.CharField(max_length=255)
    organisation_name = models.CharField(max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('person_name'),
        FieldPanel('organisation_name'),
    ]


class GoogleAdGrantsAccreditations(Orderable):
    page = ParentalKey('torchbox.GoogleAdGrantsPage', related_name="accreditations")
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]


class GoogleAdGrantsPage(Page):
    intro = RichTextField()
    form_title = models.CharField(max_length=255)
    form_subtitle = models.CharField(max_length=255)
    form_button_text = models.CharField(max_length=255)
    to_address = models.EmailField(
        verbose_name='to address', blank=True,
        help_text="Optional - form submissions will be emailed to this address"
    )
    body = RichTextField()
    grants_managed_title = models.CharField(max_length=255)
    call_to_action_title = models.CharField(max_length=255, blank=True)
    call_to_action_embed_url = models.URLField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body')
    ]

    def get_context(self, request, *args, **kwargs):
        form = GoogleAdGrantApplicationForm()
        context = super(GoogleAdGrantsPage, self).get_context(request, *args, **kwargs)
        context['form'] = form
        return context

    def serve(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            form = GoogleAdGrantApplicationForm(request.POST)
            if form.is_valid():
                form.save()

                if self.to_address:
                    subject = "{} form submission".format(self.title)
                    content = '\n'.join([x[1].label + ': ' + str(form.data.get(x[0])) for x in form.fields.items()])
                    send_mail(subject, content, [self.to_address],)
                return render(
                    request,
                    'torchbox/includes/ad_grant_application_landing.html',
                    {'self': self, 'form': form}
                )
            else:
                return render(
                    request,
                    'torchbox/includes/ad_grant_application_form.html',
                    {'self': self, 'form': form}
                )
        else:
            return super(GoogleAdGrantsPage, self).serve(request)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
        MultiFieldPanel([
            FieldPanel('form_title'),
            FieldPanel('form_subtitle'),
            FieldPanel('form_button_text'),
            FieldPanel('to_address'),
        ], "Application Form"),
        MultiFieldPanel([
            FieldPanel('grants_managed_title'),
            InlinePanel('grants_managed', label="Grants Managed")
        ], "Grants Managed Section"),
        InlinePanel('quotes', label="Quotes"),
        MultiFieldPanel([
            FieldPanel('call_to_action_title'),
            FieldPanel('call_to_action_embed_url'),
            InlinePanel('accreditations', label="Accreditations")
        ], "Call To Action")
    ]


class AbstractBaseMarketingLandingPageRelatedLink(Orderable, RelatedLink):
    email_link = models.EmailField("Email link", blank=True,
                                   help_text="Enter email address only, without 'mailto:'")

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        elif self.link_external:
            return self.link_external
        else:
            return "mailto:{}".format(self.email_link)

    panels = RelatedLink.panels + [
        FieldPanel('email_link')
    ]

    class Meta:
        abstract = True


class MarketingLandingPageHeaderRelatedLink(AbstractBaseMarketingLandingPageRelatedLink):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='header_related_links')


class MarketingLandingPageIntroRelatedLink(AbstractBaseMarketingLandingPageRelatedLink):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='intro_related_links')


class MarketingLandingPagePageClients(Orderable, RelatedLink):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='clients')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = RelatedLink.panels + [
        ImageChooserPanel('image')
    ]


class MarketingLandingPageFeaturedItem(Orderable):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='featured_items')
    related_page = models.ForeignKey('wagtailcore.Page', related_name='+')

    panels = [
        PageChooserPanel('related_page', ['blog.BlogPage', 'work.WorkPage'])
    ]


class MarketingLandingPage(Page):
    intro = models.TextField('header text', blank=True)
    hero_video_id = models.IntegerField(blank=True, null=True, help_text="Optional. The numeric ID of a Vimeo video to replace the background image.")
    hero_video_poster_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro_subtitle = models.CharField('intro subtitle', max_length=255, blank=True)

    class Meta:
        verbose_name = "Marketing Landing Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro'),
        FieldPanel('hero_video_id'),
        ImageChooserPanel('hero_video_poster_image'),
        InlinePanel('header_related_links', label="Header related items"),
        FieldPanel('intro_subtitle'),
        InlinePanel('intro_related_links', label="Intro related items"),
        InlinePanel('featured_items', label="Featured Items"),
        InlinePanel('clients', label="Clients"),
    ]


# Contact page
class ContactFormField(AbstractFormField):
    page = ParentalKey('Contact', related_name='form_fields')


class ContactLandingPageRelatedLinkButton(Orderable, RelatedLink):
    page = ParentalKey('torchbox.Contact', related_name='related_link_buttons')


@method_decorator(never_cache, name='serve')
class Contact(WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True)
    main_image = models.ForeignKey('torchbox.TorchboxImage', null=True,
                                   blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    landing_image = models.ForeignKey('torchbox.TorchboxImage', null=True,
                                      blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    thank_you_text = models.CharField(max_length=255, help_text='e.g. Thanks!')
    thank_you_follow_up = models.CharField(max_length=255, help_text='e.g. We\'ll be in touch')
    landing_page_button_title = models.CharField(max_length=255, blank=True)
    landing_page_button_link = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, related_name='+',
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Contact Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('main_image'),
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email"),
        MultiFieldPanel([
            ImageChooserPanel('landing_image'),
            FieldPanel('thank_you_text'),
            FieldPanel('thank_you_follow_up'),
            PageChooserPanel('landing_page_button_link'),
            FieldPanel('landing_page_button_title'),
        ], "Landing page"),
    ]


@register_setting
class GlobalSettings(BaseSetting):

    contact_telephone = models.CharField(max_length=255, help_text='Telephone')
    contact_email = models.EmailField(max_length=255, help_text='Email address')
    contact_twitter = models.CharField(max_length=255, help_text='Twitter')
    email_newsletter_teaser = models.CharField(max_length=255, help_text='Text that sits above the email newsletter')
    oxford_address_title = models.CharField(max_length=255, help_text='Full address')
    oxford_address = models.CharField(max_length=255, help_text='Full address')
    oxford_address_link = models.URLField(max_length=255, help_text='Link to google maps')
    oxford_address_svg = models.CharField(max_length=9000, help_text='Paste SVG code here')
    bristol_address_title = models.CharField(max_length=255, help_text='Full address')
    bristol_address = models.CharField(max_length=255, help_text='Full address')
    bristol_address_link = models.URLField(max_length=255, help_text='Link to google maps')
    bristol_address_svg = models.CharField(max_length=9000, help_text='Paste SVG code here')
    phili_address_title = models.CharField(max_length=255, help_text='Full address')
    phili_address = models.CharField(max_length=255, help_text='Full address')
    phili_address_link = models.URLField(max_length=255, help_text='Link to google maps')
    phili_address_svg = models.CharField(max_length=9000, help_text='Paste SVG code here')

    # Contact widget
    contact_person = models.ForeignKey(
        'people.PersonPage', related_name='+', null=True,
        on_delete=models.SET_NULL,
        help_text="Ensure this person has telephone and email fields set")
    contact_widget_intro = models.TextField()
    contact_widget_call_to_action = models.TextField()
    contact_widget_button_text = models.TextField()

    class Meta:
        verbose_name = 'Global Settings'

    panels = [
        FieldPanel('contact_telephone'),
        FieldPanel('contact_email'),
        FieldPanel('contact_twitter'),
        FieldPanel('email_newsletter_teaser'),
        FieldPanel('oxford_address_title'),
        FieldPanel('oxford_address'),
        FieldPanel('oxford_address_link'),
        FieldPanel('oxford_address_svg'),
        FieldPanel('bristol_address_title'),
        FieldPanel('bristol_address'),
        FieldPanel('bristol_address_link'),
        FieldPanel('bristol_address_svg'),
        FieldPanel('phili_address_title'),
        FieldPanel('phili_address'),
        FieldPanel('phili_address_link'),
        FieldPanel('phili_address_svg'),

        MultiFieldPanel([
            PageChooserPanel('contact_person'),
            FieldPanel('contact_widget_intro'),
            FieldPanel('contact_widget_call_to_action'),
            FieldPanel('contact_widget_button_text'),
        ], 'Contact widget')
    ]


class SubMenuItemBlock(StreamBlock):
    subitem = PageChooserBlock()


class MenuItemBlock(StructBlock):
    page = PageChooserBlock()
    subitems = SubMenuItemBlock()

    class Meta:
        template = "torchbox/includes/menu_item.html"


class MenuBlock(StreamBlock):
    items = MenuItemBlock()


@register_setting
class MainMenu(BaseSetting):
    menu = StreamField(MenuBlock(), blank=True)

    panels = [
        StreamFieldPanel('menu'),
    ]
