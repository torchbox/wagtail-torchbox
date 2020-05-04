from django.db import models

import graphene
from grapple.helpers import register_query_field
from grapple.models import (GraphQLCollection, GraphQLForeignKey, GraphQLInt,
                            GraphQLString)
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel


@register_query_field('service', query_params={
    'name': graphene.String()
})
class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField()
    preferred_contact = models.ForeignKey(
        'people.Contact',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    contact_reasons = models.ForeignKey(
        'people.ContactReasonsList',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order']

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('sort_order'),
        SnippetChooserPanel('preferred_contact'),
        SnippetChooserPanel('contact_reasons')
    ]

    graphql_fields = [
        GraphQLString('name'),
        GraphQLString('slug'),
        GraphQLString('description'),
        GraphQLInt('sort_order'),
        GraphQLForeignKey('preferred_contact', 'people.Contact'),
        GraphQLCollection(GraphQLForeignKey, 'contact_reasons', 'people.ContactReasonsList')
    ]
