from modelcluster.fields import ParentalKey
from wagtail.models import Page


# Copied from Wagtail and added support for ParentalManyToMany fields
def get_object_usage(obj):
    "Returns a queryset of pages that link to a particular object"

    pages = Page.objects.none()

    # get all the relation objects for obj
    relations = [
        f
        for f in type(obj)._meta.get_fields(include_hidden=True)
        if (f.one_to_many or f.one_to_one or f.many_to_many) and f.auto_created
    ]
    for relation in relations:
        related_model = relation.related_model

        # if the relation is between obj and a page, get the page
        if issubclass(related_model, Page):
            pages |= Page.objects.filter(
                id__in=related_model._base_manager.filter(
                    **{relation.field.name: obj.id}
                ).values_list("id", flat=True)
            )
        else:
            # if the relation is between obj and an object that has a page as a
            # property, return the page
            for f in related_model._meta.fields:
                if isinstance(f, ParentalKey) and issubclass(
                    f.remote_field.model, Page
                ):
                    pages |= Page.objects.filter(
                        id__in=related_model._base_manager.filter(
                            **{relation.field.name: obj.id}
                        ).values_list(f.attname, flat=True)
                    )

    return pages
