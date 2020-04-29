from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from grapple.models import (
    GraphQLString, GraphQLBoolean, GraphQLForeignKey, GraphQLImage, GraphQLPage,
    GraphQLCollection
)
from tbx.blog.models import BlogIndexPage
from tbx.work.models import WorkIndexPage
from tbx.utils.models import TorchboxPage


class BaseServicePage(TorchboxPage):
    theme = models.CharField(max_length=255, choices=(
        ('light', 'Light'),
        ('coral', 'Coral'),
        ('dark', 'Dark'),
        ('dark--transparent', 'Dark with transparent header'),
    ), default='light')

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

    content_panels = Page.content_panels + [
        FieldPanel('theme'),
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

    class Meta:
        abstract = True

    @property
    def blog_index_url(self):
        page = BlogIndexPage.objects.first()
        if page:
            return page.url
        return ''

    @property
    def work_index_url(self):
        page = WorkIndexPage.objects.first()
        if page:
            return page.url
        return ''

    graphql_fields = TorchboxPage.graphql_fields + [
        GraphQLString('theme'),
        GraphQLString('strapline'),
        GraphQLString('greeting_image_type'),
        GraphQLString('heading_for_key_points'),
        GraphQLForeignKey('contact', 'people.Contact'),
        GraphQLBoolean('use_process_block_image'),
        GraphQLString('heading_for_processes'),
        GraphQLString('key_points_section_title'),
        GraphQLString('testimonials_section_title'),
        GraphQLString('case_studies_section_title'),
        GraphQLString('blogs_section_title'),
        GraphQLString('process_section_title'),
        GraphQLString('blog_index_url'),
        GraphQLString('work_index_url'),

        GraphQLCollection(GraphQLForeignKey, 'key_points', 'services.ServicePageKeyPoint'),
        GraphQLCollection(GraphQLForeignKey, 'client_logos', 'services.ServicePageClientLogo'),
        GraphQLCollection(GraphQLForeignKey, 'usa_client_logos', 'services.ServicePageUSAClientLogo'),
        GraphQLCollection(GraphQLForeignKey, 'testimonials', 'services.ServicePageTestimonial'),
        GraphQLCollection(GraphQLForeignKey, 'featured_case_studies', 'work.WorkPage', source='featured_case_studies.case_study'),
        GraphQLCollection(GraphQLForeignKey, 'featured_blog_posts', 'blog.BlogPage', source='featured_blog_posts.blog_post'),
        GraphQLCollection(GraphQLForeignKey, 'processes', 'services.ServicePageProcess'),
    ]


class BaseServicePageKeyPoint(models.Model):
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

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLString('text'),
        GraphQLPage('linked_page'),
    ]


class BaseServicePageClientLogo(models.Model):
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        on_delete=models.CASCADE,
    )

    panels = [
        ImageChooserPanel('image'),
    ]

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLImage('image')
    ]


class BaseServicePageUSAClientLogo(models.Model):
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        on_delete=models.CASCADE,
    )

    panels = [
        ImageChooserPanel('image'),
    ]

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLImage('image')
    ]


class BaseServicePageTestimonial(models.Model):
    quote = models.TextField()
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLString('quote'),
        GraphQLString('name'),
        GraphQLString('role'),
    ]


class BaseServicePageFeaturedCaseStudy(models.Model):
    case_study = models.ForeignKey('work.WorkPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('case_study'),
    ]

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLForeignKey('case_study', 'work.WorkPage')
    ]


class BaseServicePageFeaturedBlogPost(models.Model):
    blog_post = models.ForeignKey('blog.BlogPage', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('blog_post'),
    ]

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLForeignKey('blog_post', 'blog.BlogPage')
    ]


class BaseServicePageProcess(models.Model):
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

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLString('title'),
        GraphQLString('description'),
        GraphQLPage('page_link'),
        GraphQLString('page_link_label'),
    ]


# Service page
class ServicePage(BaseServicePage):
    service = models.OneToOneField('taxonomy.Service', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to this service in taxonomy")

    content_panels = BaseServicePage.content_panels.copy()
    content_panels.insert(1, FieldPanel('service'))

    subpage_types = ['SubServicePage']

    graphql_fields = BaseServicePage.graphql_fields + [
        GraphQLForeignKey("service", 'taxonomy.Service')
    ]


class ServicePageKeyPoint(Orderable, BaseServicePageKeyPoint):
    page = ParentalKey(ServicePage, related_name='key_points')


class ServicePageClientLogo(Orderable, BaseServicePageClientLogo):
    page = ParentalKey(ServicePage, related_name='client_logos')


class ServicePageUSAClientLogo(Orderable, BaseServicePageUSAClientLogo):
    page = ParentalKey(ServicePage, related_name='usa_client_logos')


class ServicePageTestimonial(Orderable, BaseServicePageTestimonial):
    page = ParentalKey(ServicePage, related_name='testimonials')


class ServicePageFeaturedCaseStudy(Orderable, BaseServicePageFeaturedCaseStudy):
    page = ParentalKey(ServicePage, related_name='featured_case_studies')


class ServicePageFeaturedBlogPost(Orderable, BaseServicePageFeaturedBlogPost):
    page = ParentalKey(ServicePage, related_name='featured_blog_posts')


class ServicePageProcess(Orderable, BaseServicePageProcess):
    page = ParentalKey(ServicePage, related_name='processes')


# Sub-service page
class SubServicePage(BaseServicePage):
    show_automatic_blog_listing = models.BooleanField(default=False)
    show_automatic_case_studies_listing = models.BooleanField(default=False)
    parent_page_types = ['ServicePage']

    content_panels = BaseServicePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('show_automatic_blog_listing'),
                FieldPanel('show_automatic_case_studies_listing'),
            ],
            heading="Listings settings",
            classname="collapsible"
        ),
    ]

    @property
    def service(self):
        service_page = ServicePage.objects.ancestor_of(self).live().last()

        if service_page:
            return service_page.service

    graphql_fields = BaseServicePage.graphql_fields + [
        GraphQLBoolean('show_automatic_blog_listing'),
        GraphQLBoolean('show_automatic_case_studies_listing'),

        # Service page overrides
        GraphQLForeignKey('service', 'taxonomy.Service'),
        GraphQLCollection(GraphQLForeignKey, 'key_points', 'services.SubServicePageKeyPoint'),
        GraphQLCollection(GraphQLForeignKey, 'client_logos', 'services.SubServicePageClientLogo'),
        GraphQLCollection(GraphQLForeignKey, 'usa_client_logos', 'services.SubServicePageUSAClientLogo'),
        GraphQLCollection(GraphQLForeignKey, 'testimonials', 'services.SubServicePageTestimonial'),
        GraphQLCollection(GraphQLForeignKey, 'processes', 'services.SubServicePageProcess'),
    ]


class SubServicePageKeyPoint(Orderable, BaseServicePageKeyPoint):
    page = ParentalKey(SubServicePage, related_name='key_points')


class SubServicePageClientLogo(Orderable, BaseServicePageClientLogo):
    page = ParentalKey(SubServicePage, related_name='client_logos')


class SubServicePageUSAClientLogo(Orderable, BaseServicePageUSAClientLogo):
    page = ParentalKey(SubServicePage, related_name='usa_client_logos')


class SubServicePageTestimonial(Orderable, BaseServicePageTestimonial):
    page = ParentalKey(SubServicePage, related_name='testimonials')


class SubServicePageFeaturedCaseStudy(Orderable, BaseServicePageFeaturedCaseStudy):
    page = ParentalKey(SubServicePage, related_name='featured_case_studies')


class SubServicePageFeaturedBlogPost(Orderable, BaseServicePageFeaturedBlogPost):
    page = ParentalKey(SubServicePage, related_name='featured_blog_posts')


class SubServicePageProcess(Orderable, BaseServicePageProcess):
    page = ParentalKey(SubServicePage, related_name='processes')
