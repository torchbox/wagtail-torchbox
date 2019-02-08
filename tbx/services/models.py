from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         PageChooserPanel, StreamFieldPanel, MultiFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel


# class ServicePageHeroLink(Orderable):
#     page = ParentalKey('services.ServicePage', related_name='hero_links')
#     label = models.TextField()
#     linked_section= models.CharField(max_length=6, choices=(
#         ('key_points', 'Key Points'),
#         ('contact', 'Contact'),
#         ('testimonials','Testimonials'),
#         ('work','Work / Case-Studies'),
#         ('blogs','Blogs'),
#     ), default='key_points')


class ServicePageKeyPoint(Orderable):
    page = ParentalKey('services.ServicePage', related_name='key_points')
    text = models.CharField(max_length=255)
    linked_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = [
        PageChooserPanel('linked_page'),
    ]


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


class ServicePageProcess(Orderable):
    page = ParentalKey('services.ServicePage', related_name='processes')
    title = models.TextField()
    description = models.TextField()
    page_link = models.ForeignKey('wagtailcore.Page', on_delete=models.CASCADE, blank=True, null=True)
    page_link_label = models.TextField(blank=True, null=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('description', classname="full title"),
        MultiFieldPanel(
            [
                FieldPanel('page_link_label', classname="full title"),
                FieldPanel('page_link', classname="full title"),
            ],
            heading="Link"
        )
    ]


class ServicePage(Page):
    service = models.OneToOneField('taxonomy.Service', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to this service in taxonomy")
    is_darktheme = models.BooleanField(default=False)
    strapline = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    heading_for_key_points = RichTextField()
    contact = models.ForeignKey('people.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    use_process_block_image = models.BooleanField(default=False)

    # Section titles
    key_points_section_title = models.TextField(blank=True, default="Services")
    testimonials_section_title = models.TextField(blank=True, default="Clients")
    case_studies_section_title = models.TextField(blank=True, default="Work") 
    blogs_section_title = models.TextField(blank=True, default="Thinking")
    process_section_title = models.TextField(blank=True, default="Process")

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('service'),
        FieldPanel('is_darktheme'),
        MultiFieldPanel(
            [
                FieldPanel('strapline', classname="full title"),
                FieldPanel('intro', classname="full"),
            ],
            heading="Hero",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('key_points_section_title', classname="full"),
                FieldPanel('heading_for_key_points', classname="full"),
                InlinePanel('key_points', label="Key points"),
            ],
            heading="Key Points",
            classname="collapsible"
        ),
        SnippetChooserPanel('contact'),
        MultiFieldPanel(
            [
                FieldPanel('testimonials_section_title', classname="full"),
                InlinePanel('client_logos', label="Client logos"),
                InlinePanel('usa_client_logos', label="Client logos (for USA users)"),
                InlinePanel('testimonials', label="Testimonials"),
            ],
            heading="Testimonials",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('process_section_title', classname="full"),
                FieldPanel('use_process_block_image', classname="full"),
                InlinePanel('processes', label="Processes")
            ],
            heading="Processes",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('case_studies_section_title', classname="full"),
                InlinePanel('featured_case_studies', label="Featured case studies"),
            ],
            heading="Work",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('blogs_section_title', classname="full"),
                InlinePanel('featured_blog_posts', label="Featured blog posts"),
            ],
            heading="Blogs",
            classname="collapsible"
        ),
    ]


class SubServicePage(ServicePage):
    pass
