from django.core import exceptions as django_exceptions
from django.db import models

from tbx.core.utils import models as utils_models
from tbx.courses import blocks as tbx_course_blocks
from wagtail import fields as wagtail_fields
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.search import index

INTRO_RICHTEXT_FEATURES = ["bold", "italic", "link", "document-link", "strikethrough"]


class CourseLandingPage(utils_models.SocialFields, wagtail_models.Page):
    # stubbed out for now, is incoming

    template = "patterns/pages/courses/course_landing_page.html"

    content_panels = wagtail_models.Page.content_panels + []

    promote_panels = [
        panels.MultiFieldPanel(
            wagtail_models.Page.promote_panels, "Common page configuration"
        ),
        panels.MultiFieldPanel(
            utils_models.SocialFields.promote_panels, "Social fields"
        ),
    ]


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

    def get_context(self, request):
        context = super().get_context(request)
        return context
