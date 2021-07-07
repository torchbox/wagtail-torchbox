from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from tbx.blog.models import BlogIndexPage
from tbx.work.models import WorkIndexPage


class BaseServicePage(Page):
    theme = models.CharField(
        max_length=255,
        choices=(
            ("light", "Light"),
            ("coral", "Coral"),
            ("dark", "Dark"),
            ("dark--transparent", "Dark with transparent header"),
        ),
        default="light",
    )

    strapline = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    greeting_image_type = models.CharField(
        max_length=255,
        choices=(
            ("woman-left", "Woman (Left Aligned)"),
            ("man-left", "Man (Left aligned)"),
            ("wagtail", "Wagtail (Right aligned)"),
        ),
        default="woman-left",
        blank=True,
        null=True,
    )

    heading_for_key_points = RichTextField(blank=True)
    contact = models.ForeignKey(
        "people.Contact",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    contact_reasons = models.ForeignKey(
        "people.ContactReasonsList",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    use_process_block_image = models.BooleanField(default=False)
    heading_for_processes = models.TextField(blank=True, null=True)
    process_section_cta = RichTextField(
        verbose_name="Process section CTA",
        blank=True,
        help_text="An opportunity to use a more flexible call to action, if the main “Contact” fields aren’t suitable",
    )

    # Section titles
    key_points_section_title = models.TextField(blank=True, default="Services")
    testimonials_section_title = models.TextField(blank=True, default="Clients")
    case_studies_section_title = models.TextField(blank=True, default="Work")
    blogs_section_title = models.TextField(blank=True, default="Thinking")
    process_section_title = models.TextField(blank=True, default="Process")

    content_panels = Page.content_panels + [
        FieldPanel("theme"),
        MultiFieldPanel(
            [
                FieldPanel("strapline", classname="full title"),
                FieldPanel("intro", classname="full"),
                FieldPanel("greeting_image_type", classname="full"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("key_points_section_title", classname="full"),
                FieldPanel("heading_for_key_points", classname="full"),
                InlinePanel("key_points", label="Key points"),
            ],
            heading="Key Points",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [SnippetChooserPanel("contact"), SnippetChooserPanel("contact_reasons")],
            heading="Contact",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("testimonials_section_title", classname="full"),
                InlinePanel("client_logos", label="Client logos"),
                InlinePanel("usa_client_logos", label="Client logos (for USA users)"),
                InlinePanel("testimonials", label="Testimonials"),
            ],
            heading="Testimonials",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("process_section_title", classname="full"),
                FieldPanel("heading_for_processes", classname="full"),
                FieldPanel("use_process_block_image", classname="full"),
                InlinePanel("processes", label="Processes"),
                FieldPanel("process_section_cta", classname="full"),
            ],
            heading="Processes",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("case_studies_section_title", classname="full"),
                InlinePanel("featured_case_studies", label="Featured case studies"),
            ],
            heading="Work",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("blogs_section_title", classname="full"),
                InlinePanel("featured_blog_posts", label="Featured blog posts"),
            ],
            heading="Thinking",
            classname="collapsible",
        ),
    ]

    class Meta:
        abstract = True

    def get_featured_blog_posts(self):
        """Format the featured blog posts for the template."""
        return [
            {
                "title": featured.blog_post.title,
                "url": featured.blog_post.url,
                "author": featured.blog_post.first_author,
                "date": featured.blog_post.date,
            }
            for featured in self.featured_blog_posts.all()
            if featured.blog_post.live
        ]

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            featured_blog_posts=self.get_featured_blog_posts(),
            blog_index_page=BlogIndexPage.objects.live().first(),
            work_index_page=WorkIndexPage.objects.live().first(),
        )
        return context


class BaseServicePageKeyPoint(models.Model):
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
        PageChooserPanel("linked_page"),
    ]

    class Meta:
        abstract = True


class BaseServicePageClientLogo(models.Model):
    image = models.ForeignKey("torchbox.TorchboxImage", on_delete=models.CASCADE,)

    panels = [
        ImageChooserPanel("image"),
    ]

    class Meta:
        abstract = True


class BaseServicePageUSAClientLogo(models.Model):
    image = models.ForeignKey("torchbox.TorchboxImage", on_delete=models.CASCADE,)

    panels = [
        ImageChooserPanel("image"),
    ]

    class Meta:
        abstract = True


class BaseServicePageTestimonial(models.Model):
    quote = models.TextField()
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    class Meta:
        abstract = True


class BaseServicePageFeaturedCaseStudy(models.Model):
    case_study = models.ForeignKey("work.WorkPage", on_delete=models.CASCADE)

    panels = [
        PageChooserPanel("case_study"),
    ]

    class Meta:
        abstract = True


class BaseServicePageFeaturedBlogPost(models.Model):
    blog_post = models.ForeignKey("blog.BlogPage", on_delete=models.CASCADE)

    panels = [
        PageChooserPanel("blog_post"),
    ]

    class Meta:
        abstract = True


class BaseServicePageProcess(models.Model):
    title = models.TextField()
    description = models.TextField()
    page_link = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, blank=True, null=True
    )
    page_link_label = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel("title", classname="title"),
        FieldPanel("description", classname="title"),
        PageChooserPanel("page_link"),
        FieldPanel("page_link_label"),
    ]

    class Meta:
        abstract = True


# Service page


class ServicePage(BaseServicePage):
    template = "patterns/pages/service/service.html"

    service = models.OneToOneField(
        "taxonomy.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Link to this service in taxonomy",
    )

    content_panels = BaseServicePage.content_panels.copy()
    content_panels.insert(1, FieldPanel("service"))

    subpage_types = ["SubServicePage"]


class ServicePageKeyPoint(Orderable, BaseServicePageKeyPoint):
    page = ParentalKey(ServicePage, related_name="key_points")


class ServicePageClientLogo(Orderable, BaseServicePageClientLogo):
    page = ParentalKey(ServicePage, related_name="client_logos")


class ServicePageUSAClientLogo(Orderable, BaseServicePageUSAClientLogo):
    page = ParentalKey(ServicePage, related_name="usa_client_logos")


class ServicePageTestimonial(Orderable, BaseServicePageTestimonial):
    page = ParentalKey(ServicePage, related_name="testimonials")


class ServicePageFeaturedCaseStudy(Orderable, BaseServicePageFeaturedCaseStudy):
    page = ParentalKey(ServicePage, related_name="featured_case_studies")


class ServicePageFeaturedBlogPost(Orderable, BaseServicePageFeaturedBlogPost):
    page = ParentalKey(ServicePage, related_name="featured_blog_posts")


class ServicePageProcess(Orderable, BaseServicePageProcess):
    page = ParentalKey(ServicePage, related_name="processes")


# Sub-service page


class SubServicePage(BaseServicePage):
    template = "patterns/pages/service/service.html"

    parent_page_types = ["ServicePage"]

    @property
    def service(self):
        service_page = ServicePage.objects.ancestor_of(self).live().last()

        if service_page:
            return service_page.service


class SubServicePageKeyPoint(Orderable, BaseServicePageKeyPoint):
    page = ParentalKey(SubServicePage, related_name="key_points")


class SubServicePageClientLogo(Orderable, BaseServicePageClientLogo):
    page = ParentalKey(SubServicePage, related_name="client_logos")


class SubServicePageUSAClientLogo(Orderable, BaseServicePageUSAClientLogo):
    page = ParentalKey(SubServicePage, related_name="usa_client_logos")


class SubServicePageTestimonial(Orderable, BaseServicePageTestimonial):
    page = ParentalKey(SubServicePage, related_name="testimonials")


class SubServicePageFeaturedCaseStudy(Orderable, BaseServicePageFeaturedCaseStudy):
    page = ParentalKey(SubServicePage, related_name="featured_case_studies")


class SubServicePageFeaturedBlogPost(Orderable, BaseServicePageFeaturedBlogPost):
    page = ParentalKey(SubServicePage, related_name="featured_blog_posts")


class SubServicePageProcess(Orderable, BaseServicePageProcess):
    page = ParentalKey(SubServicePage, related_name="processes")
