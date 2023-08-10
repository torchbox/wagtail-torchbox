import json
from functools import wraps

from django.core.exceptions import FieldError


def for_each_page_revision(*model_names):
    """
    A data migration decorator which iterates all revisions of the specified page model and
    passes the deserialised content to the function.

    If the function returns a non-None value, this value will replace the existing content and
    the revision will be saved.

    For example, the following adds a new field into all revisions of the 'myapp.MyPage' model:

    @for_each_page_revision('myapp.MyPage')
    def migrate_revision(page, revision_content):
        revision_content['foo'] = 'bar'
        return revision_content
    """

    def wrapper(fn):
        @wraps(fn)
        def wrapper(apps, schema_editor):
            ContentType = apps.get_model("contenttypes.ContentType")

            try:
                PageRevision = apps.get_model("wagtailcore.Revision")
            except LookupError:
                # In previous versions of Wagtail, this model was `PageRevision`
                PageRevision = apps.get_model("wagtailcore.PageRevision")

            content_types = [
                ContentType.objects.get_for_model(apps.get_model(model_name))
                for model_name in model_names
            ]

            try:
                revisions = PageRevision.objects.filter(content_type__in=content_types)
            except FieldError:
                # In previous versions of Wagtail, the content_type field does not exist
                revisions = PageRevision.objects.filter(
                    page__content_type__in=content_types
                ).select_related("page")

            for revision in revisions:
                content = json.loads(revision.content_json)
                new_content = fn(revision.page, content)
                if new_content is not None:
                    revision.content_json = json.dumps(new_content)
                    revision.save()

        return wrapper

    return wrapper
