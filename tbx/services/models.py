from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from tbx.blog.models import BlogIndexPage
from tbx.core.blocks import PageSectionStoryBlock
from tbx.core.utils.models import SocialFields
from tbx.propositions.models import PropositionPage
from tbx.work.models import WorkIndexPage
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index


class BaseServicePage(SocialFields, Page):
    theme = models.CharField(
        max_length=255,
        choices=(
            ("light", "Light"),
            ("coral", "Coral"),
            ("dark", "Dark"),
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
    processes_section_embed_url = models.URLField("Embed URL", blank=True)

    # Section titles
    key_points_section_title = models.TextField(blank=True, default="Services")
    testimonials_section_title = models.TextField(
        blank=True,
        default="Clients",
        help_text="Leave this field empty to hide the testimonials section.",
    )
    case_studies_section_title = models.TextField(
        blank=True,
        default="Work",
        help_text="Leave this field empty to hide the case studies section.",
    )
    blogs_section_title = models.TextField(blank=True, default="Thinking")
    process_section_title = models.TextField(blank=True, default="Process")

    content_panels = Page.content_panels + [
        FieldPanel("theme"),
        MultiFieldPanel(
            [
                FieldPanel("strapline", classname="title"),
                FieldPanel("intro"),
                FieldPanel("greeting_image_type"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("key_points_section_title"),
                FieldPanel("heading_for_key_points"),
                InlinePanel("key_points", label="Key points"),
            ],
            heading="Key Points",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [FieldPanel("contact"), FieldPanel("contact_reasons")],
            heading="Contact",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("testimonials_section_title"),
                InlinePanel("client_logos", label="Client logos"),
                InlinePanel("usa_client_logos", label="Client logos (for USA users)"),
                InlinePanel("testimonials", label="Testimonials"),
            ],
            heading="Testimonials",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("process_section_title"),
                FieldPanel("heading_for_processes"),
                FieldPanel("use_process_block_image"),
                FieldPanel("processes_section_embed_url"),
                InlinePanel("processes", label="Processes"),
                FieldPanel("process_section_cta"),
            ],
            heading="Processes",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("case_studies_section_title"),
                InlinePanel("featured_case_studies", label="Featured case studies"),
            ],
            heading="Work",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("blogs_section_title"),
                InlinePanel("featured_blog_posts", label="Featured blog posts"),
            ],
            heading="Thinking",
            classname="collapsible",
        ),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(SocialFields.promote_panels, "Social fields"),
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

    def get_featured_case_studies(self):
        """Format the featured case studies data for the template."""
        return [
            {
                "title": f.case_study.title,
                "subtitle": f.case_study.client,
                "description": f.case_study.listing_summary,
                "url": f.case_study.url,
                "image": f.case_study.homepage_image,
            }
            for f in self.featured_case_studies.all()
            if f.case_study
        ]

    @property
    def filter_by(self):
        if self.service:
            return self.service.slug

        # If no service defined, don't filter by anything
        return ""


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
        FieldPanel("linked_page"),
    ]

    class Meta:
        abstract = True


class BaseServicePageClientLogo(models.Model):
    image = models.ForeignKey(
        "images.CustomImage",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("image"),
    ]

    class Meta:
        abstract = True


class BaseServicePageUSAClientLogo(models.Model):
    image = models.ForeignKey(
        "images.CustomImage",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("image"),
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
        FieldPanel("case_study"),
    ]

    class Meta:
        abstract = True


class BaseServicePageFeaturedBlogPost(models.Model):
    blog_post = models.ForeignKey("blog.BlogPage", on_delete=models.CASCADE)

    panels = [
        FieldPanel("blog_post"),
    ]

    class Meta:
        abstract = True


class BaseServicePageProcess(models.Model):
    title = models.TextField()
    description = models.TextField()
    external_link = models.URLField("External link", blank=True)
    page_link = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, blank=True, null=True
    )
    link_label = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel("title", classname="title"),
        FieldPanel("description", classname="title"),
        FieldPanel("page_link"),
        FieldPanel("external_link"),
        FieldPanel("link_label"),
    ]

    @property
    def link(self):
        if self.external_link:
            return self.external_link
        if self.page_link:
            return self.page_link.get_url()

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
    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
    )

    content_panels = BaseServicePage.content_panels.copy()
    content_panels.insert(1, FieldPanel("service"))
    content_panels.append(FieldPanel("call_to_action"))

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

    parent_page_types = ["ServicePage", "propositions.PropositionPage"]

    # Prevent editors from using the page type until we fully remove it
    is_creatable = False

    content = StreamField(
        PageSectionStoryBlock(), blank=True, use_json_field=True, collapsed=True
    )

    search_fields = BaseServicePage.search_fields + [
        index.SearchField("content"),
    ]

    content_panels = BaseServicePage.content_panels + [
        FieldPanel("content", heading="Content"),
    ]

    @cached_property
    def service(self):
        try:
            return (
                PropositionPage.objects.ancestor_of(self)
                .defer_streamfields()
                .select_related("service")
                .last()
            ).service
        except AttributeError:
            pass
        try:
            return (
                ServicePage.objects.ancestor_of(self)
                .defer_streamfields()
                .select_related("service")
                .last()
            ).service
        except AttributeError:
            pass


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
