from django import forms
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
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

from grapple.models import GraphQLString, GraphQLPage, GraphQLForeignKey, GraphQLStreamfield, GraphQLCollection
from grapple.helpers import register_streamfield_block, register_query_field
from wagtailgatsby.models import GatsbyImage, GatsbyImageRendition

from tbx.utils.models import TorchboxPage
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.SET_NULL,
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

    graphql_fields = [
        GraphQLString('telephone'),
        GraphQLString('email'),
        GraphQLString('address_1'),
        GraphQLString('address_2'),
        GraphQLString('city'),
        GraphQLString('country'),
        GraphQLString('post_code'),
    ]


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
    advert = models.ForeignKey('torchbox.Advert', on_delete=models.CASCADE, related_name='+')

    graphql_fields = [
        GraphQLPage('page'),
        GraphQLForeignKey('advert', 'torchbox.Advert')
    ]


@register_snippet
class Advert(models.Model):
    page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='adverts'
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

    graphql_fields = [
        GraphQLPage('page'),
        GraphQLString('url'),
        GraphQLString('text')
    ]


# Custom image
# GatsbyImage/GatsbyImageRendition expand upon AbstractImage/Rendition
class TorchboxImage(GatsbyImage):
    credit = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'credit',
    )

    @property
    def credit_text(self):
        return self.credit

    graphql_fields = [
        GraphQLString("base64"),
        GraphQLString("tracedSVG", source="traced_SVG"),
    ]


class TorchboxRendition(GatsbyImageRendition):
    image = models.ForeignKey('TorchboxImage', on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Home Page
class HomePage(TorchboxPage):

    class Meta:
        verbose_name = "Homepage"

    content_panels = [
        FieldPanel('title', classname="full title"),
    ]


class StandardPage(TorchboxPage):
    body = StreamField(StoryBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLStreamfield('body')
    ]


# Currently hidden. These were used in the past and may be used again in the future
# @register_snippet
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Jobs index page
@register_query_field('job')
class JobIndexPageJob(Orderable):
    page = ParentalKey('torchbox.JobIndexPage', related_name='jobs')
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    url = models.URLField(null=True)
    location = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('level'),
        FieldPanel('url'),
        FieldPanel('location'),
    ]

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('level'),
        GraphQLString('url'),
        GraphQLString('location'),
    ]


class JobIndexPage(TorchboxPage):
    strapline = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('strapline', classname="full title"),
        InlinePanel('jobs', label="Jobs"),
    ]

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLString('strapline'),
        GraphQLCollection(
            GraphQLForeignKey,
            'jobs',
            JobIndexPageJob,
        )
    ]


class NotFoundPage(TorchboxPage):
    strapline = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Only allow one instance of NotFound Page
        if not self.pk and NotFoundPage.objects.exists():
            raise ValidationError('There can only be one 404 page instance')

        # Only allow a slug of /404/
        return super(NotFoundPage, self).save(*args, **kwargs)

    content_panels = Page.content_panels + [
        FieldPanel('strapline', classname="full title"),
    ]

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLString('strapline'),
    ]


# Currently hidden. These were used in the past and may be used again in the future
class GoogleAdGrantApplication(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        ordering = ['-date']


# Currently hidden. These were used in the past and may be used again in the future
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


# Currently hidden. These were used in the past and may be used again in the future
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


# Currently hidden. These were used in the past and may be used again in the future
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


# Currently hidden. These were used in the past and may be used again in the future
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


# Currently hidden. These were used in the past and may be used again in the future
class GoogleAdGrantsPage(TorchboxPage):
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

    graphql_fields = [
        GraphQLString('contact_telephone'),
        GraphQLString('contact_email'),
        GraphQLString('contact_twitter'),
        GraphQLString('email_newsletter_teaser'),
        GraphQLString('oxford_address_title'),
        GraphQLString('oxford_address'),
        GraphQLString('oxford_address_link'),
        GraphQLString('oxford_address_svg'),
        GraphQLString('bristol_address_title'),
        GraphQLString('bristol_address'),
        GraphQLString('bristol_address_link'),
        GraphQLString('bristol_address_svg'),
    ]


@register_streamfield_block
class SubMenuItemBlock(StreamBlock):
    # subitem = PageChooserBlock()
    related_listing_page = PageChooserBlock()

    graphql_fields = [
        GraphQLPage('related_listing_page')
    ]


@register_streamfield_block
class MenuItemBlock(StructBlock):
    page = PageChooserBlock()
    subitems = SubMenuItemBlock(blank=True, null=True)

    graphql_fields = [
        GraphQLPage('page'),
        GraphQLCollection(
            GraphQLForeignKey,
            'subitems',
            SubMenuItemBlock
        )
    ]


@register_streamfield_block
class MenuBlock(StreamBlock):
    items = MenuItemBlock()

    graphql_fields = [
        GraphQLCollection(
            GraphQLForeignKey,
            'items',
            MenuItemBlock
        )
    ]


@register_setting
class MainMenu(BaseSetting):
    menu = StreamField(MenuBlock(), blank=True)

    panels = [
        StreamFieldPanel('menu'),
    ]

    graphql_fields = [
        GraphQLCollection(
            GraphQLForeignKey,
            'menu',
            MenuItemBlock,
            source="menu.items"
        )
    ]
