from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class ServicePageKeyPoint(Orderable):
    page = ParentalKey('services.ServicePage', related_name='key_points')
    text = models.CharField(max_length=255)


class ServicePageClientLogo(Orderable):
    page = ParentalKey('services.ServicePage', related_name='client_logos')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        on_delete=models.CASCADE,
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class ServicePageUSAClientLogo(Orderable):
    page = ParentalKey('services.ServicePage', related_name='usa_client_logos')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        on_delete=models.CASCADE,
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class ServicePageTestimonial(Orderable):
    page = ParentalKey('services.ServicePage', related_name='testimonials')
    quote = models.TextField()
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)


class ServicePageFeaturedCaseStudy(Orderable):
    page = ParentalKey('services.ServicePage', related_name='featured_case_studies')
    case_study = models.ForeignKey('work.WorkPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('case_study'),
    ]


class ServicePageFeaturedBlogPost(Orderable):
    page = ParentalKey('services.ServicePage', related_name='featured_blog_posts')
    blog_post = models.ForeignKey('blog.BlogPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('blog_post'),
    ]


class ServicePage(Page):
    service = models.OneToOneField('taxonomy.Service', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to this service in taxonomy")
    strapline = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    heading_for_key_points = RichTextField()

    contact = models.ForeignKey('people.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('service'),
        FieldPanel('strapline', classname="full title"),
        FieldPanel('intro', classname="full"),
        FieldPanel('heading_for_key_points', classname="full"),
        InlinePanel('key_points', label="Key points"),
        SnippetChooserPanel('contact'),
        InlinePanel('client_logos', label="Client logos"),
        InlinePanel('usa_client_logos', label="Client logos (for USA users)"),
        InlinePanel('testimonials', label="Testimonials"),
        InlinePanel('featured_case_studies', label="Featured case studies"),
        InlinePanel('featured_blog_posts', label="Featured blog posts"),
    ]
