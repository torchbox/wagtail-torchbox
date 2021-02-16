from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField()
    preferred_contact = models.ForeignKey(
        "people.Contact", null=True, blank=True, on_delete=models.SET_NULL
    )
    contact_reasons = models.ForeignKey(
        "people.ContactReasonsList", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sort_order"]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("sort_order"),
        SnippetChooserPanel("preferred_contact"),
        SnippetChooserPanel("contact_reasons"),
    ]
