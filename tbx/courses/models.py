from django.core import exceptions as django_exceptions
from django.db import models

from modelcluster import fields as modelcluster_fields
from tbx.core.utils import models as utils_models
from tbx.courses import blocks as tbx_course_blocks
from wagtail import fields as wagtail_fields
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.search import index

INTRO_RICHTEXT_FEATURES = ["bold", "italic", "link", "document-link", "strikethrough"]


class CourseLandingPage(utils_models.SocialFields, wagtail_models.Page):
    # Don't offer a theme style, just set to dark
    theme = "dark"
    template = "patterns/pages/courses/course_landing_page.html"

    strapline = models.CharField(
        max_length=255,
        help_text="Words in <span> tag will display in a contrasting colour.",
    )
    sub_title = models.CharField(
        max_length=255,
        help_text="Displayed just below the strapline.",
        blank=True,
    )
    intro = wagtail_fields.RichTextField(blank=True, features=INTRO_RICHTEXT_FEATURES)
    child_page_listing_heading = models.CharField(
        max_length=255,
        help_text="A heading shown above the child pages listed.",
        blank=True,
    )
    content_panels = wagtail_models.Page.content_panels + [
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("strapline", classname="full title"),
                panels.FieldPanel("sub_title"),
                panels.FieldPanel("intro", classname="full"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        panels.FieldPanel("child_page_listing_heading"),
    ]

    promote_panels = [
        panels.MultiFieldPanel(
            wagtail_models.Page.promote_panels, "Common page configuration"
        ),
        panels.MultiFieldPanel(
            utils_models.SocialFields.promote_panels, "Social fields"
        ),
    ]

    search_fields = wagtail_models.Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("strapline"),
    ]

    def _get_subpages(self):
        subpages = (
            CourseDetailPage.objects.live()
            .descendant_of(self)
            .order_by("title")
            .only("title", "sessions", "cost", "intro")
        )
        return subpages

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["subpages"] = self._get_subpages()
        return context


class RelatedCoursePage(wagtail_models.Orderable):
    source_page = modelcluster_fields.ParentalKey(
        wagtail_models.Page, related_name="related_course_pages"
    )
    page = models.ForeignKey("courses.CourseDetailPage", on_delete=models.CASCADE)

    panels = [panels.FieldPanel("page")]


class CourseDetailPage(utils_models.SocialFields, wagtail_models.Page):
    parent_page_types = ["courses.CourseLandingPage"]

    template = "patterns/pages/courses/course_detail_page.html"

    strapline = models.CharField(
        max_length=255,
        help_text="Words in <span> tag will display in a contrasting colour.",
    )
    sessions = models.CharField(max_length=25, blank=True, help_text="e.g. 4 sessions")
    cost = models.CharField(
        max_length=255, blank=True, help_text="e.g.£999 / $1,299 per person "
    )
    intro = wagtail_fields.RichTextField(blank=True, features=INTRO_RICHTEXT_FEATURES)
    header_link = models.URLField(blank=True, help_text="e.g. https://www.example.com")
    header_link_text = models.CharField(
        max_length=255, blank=True, help_text="e.g. Visit example.com for dates"
    )

    body = wagtail_fields.StreamField(
        tbx_course_blocks.CourseDetailStoryBlock(), use_json_field=True
    )

    search_fields = wagtail_models.Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("strapline"),
    ]

    content_panels = wagtail_models.Page.content_panels + [
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("strapline", classname="full title"),
                panels.FieldPanel("sessions"),
                panels.FieldPanel("cost"),
                panels.FieldPanel("intro", classname="full"),
                panels.FieldPanel("header_link", classname="col6"),
                panels.FieldPanel("header_link_text", classname="col6"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        panels.FieldPanel("body"),
        panels.InlinePanel("related_course_pages", label="Related courses"),
    ]

    promote_panels = [
        panels.MultiFieldPanel(
            wagtail_models.Page.promote_panels, "Common page configuration"
        ),
        panels.MultiFieldPanel(
            utils_models.SocialFields.promote_panels, "Social fields"
        ),
    ]

    def clean(self):
        errors = {}

        if self.header_link and not self.header_link_text:
            errors["header_link_text"] = "You must set a text value for the link."

        if self.header_link_text and not self.header_link:
            errors["header_link"] = "You must set a link value for the header link."

        if errors:
            raise django_exceptions.ValidationError(errors)

    @property
    def related_courses(self):
        related_course_pages = self.related_course_pages.all().select_related("page")
        related_courses = [page.page for page in related_course_pages]
        return related_courses
