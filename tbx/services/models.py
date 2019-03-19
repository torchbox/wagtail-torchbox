from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
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

    panels = [
        FieldPanel('text'),
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

    panels = [
        FieldPanel('title', classname="title"),
        FieldPanel('description', classname="title"),
        PageChooserPanel('page_link'),
        FieldPanel('page_link_label'),
    ]


class ServicePage(Page):
    service = models.OneToOneField('taxonomy.Service', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to this service in taxonomy")
    is_darktheme = models.BooleanField(default=False)

    strapline = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    greeting_image_type = models.CharField(max_length=255, choices=(
        ('woman-left', 'Woman (Left Aligned)'),
        ('man-left', 'Man (Left aligned)'),
        ('wagtail', 'Wagtail (Right aligned)'),
    ), default='woman-left', blank=True, null=True)

    heading_for_key_points = RichTextField(blank=True)
    contact = models.ForeignKey('people.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    contact_reasons = models.ForeignKey('people.ContactReasonsList', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    use_process_block_image = models.BooleanField(default=False)
    heading_for_processes = models.TextField(blank=True, null=True)

    # Section titles
    key_points_section_title = models.TextField(blank=True, default="Services")
    testimonials_section_title = models.TextField(blank=True, default="Clients")
    case_studies_section_title = models.TextField(blank=True, default="Work")
    blogs_section_title = models.TextField(blank=True, default="Thinking")
    process_section_title = models.TextField(blank=True, default="Process")

    service_content_panels = [
        FieldPanel('is_darktheme'),
        MultiFieldPanel(
            [
                FieldPanel('strapline', classname="full title"),
                FieldPanel('intro', classname="full"),
                FieldPanel('greeting_image_type', classname="full")
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
        MultiFieldPanel(
            [
                SnippetChooserPanel('contact'),
                SnippetChooserPanel('contact_reasons'),
            ],
            heading="Contact",
            classname="collapsible"
        ),
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
                FieldPanel('heading_for_processes', classname="full"),
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

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('service'),
    ] + service_content_panels


class SubServicePage(ServicePage):
    parent_service = models.ForeignKey('taxonomy.Service', on_delete=models.SET_NULL, null=True, blank=True,
                                       help_text="Link to this service in taxonomy")

    content_panels = [
        FieldPanel('title'),
        FieldPanel('parent_service'),
    ] + ServicePage.service_content_panels
