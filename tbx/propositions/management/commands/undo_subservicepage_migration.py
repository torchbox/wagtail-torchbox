import logging
import re
import time
from itertools import chain

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.template.defaultfilters import pluralize

from tbx.propositions.constants import SLUG_SUFFIX, TITLE_SUFFIX
from tbx.propositions.models import SubPropositionPage
from tbx.propositions.models import (
    SubServicePageToSubPropositionPageMigration as MigrationRecord,
)
from tbx.services.models import SubServicePage
from wagtail.blocks import StreamValue
from wagtail.fields import StreamField
from wagtail.models import Page

logger = logging.getLogger(__name__)


def is_streamfield(field):
    return isinstance(field, StreamField)


def replace_link(match, ids):
    """
    Replace a link to a SubPropositionPage with a link to a SubServicePage.

    Args:
        match (re.Match): The match object returned by the regex search.
        ids (list): A list of IDs of SubPropositionPages that were
        migrated from SubServicePages.
    """
    new_page_id = int(match.group(1))
    if new_page_id in ids:
        new_page = SubPropositionPage.objects.get(pk=new_page_id)
        title_list = [new_page.title, new_page.title + f" {TITLE_SUFFIX}"]
        slug_list = [new_page.slug, new_page.slug + SLUG_SUFFIX]
        old_page_instance = SubServicePage.objects.filter(
            title__in=title_list,
            slug__in=slug_list,
        ).first()
        if old_page_instance:
            return f'<a id="{old_page_instance.pk}" linktype="page">'
    else:
        # Return the original match if no replacement is made
        return match.group(0)


def update_stream_data(data):
    """
    Recursively updates data containing links to SubPropositionPages to point to
    corresponding SubServicePages.

    This function is designed to process a nested data structure, such as a JSON
    object or a list, and replace links to SubPropositionPages with links to
    SubServicePages. It works by recursively traversing the data structure and
    performing the necessary replacements.

    Args:
        data (dict or list): The data structure containing links to SubPropositionPages
        that need to be updated.

    Returns:
        dict or list: The updated data structure with links replaced.
    """

    page_keys = [
        "link",
        "internal",
        "page_link",
        "linked_page",
        "page",
        "related_listing_page",
    ]
    new_pages_ids = SubPropositionPage.objects.all().values_list("pk", flat=True)

    if isinstance(data, list):
        new_data = []
        for item in data:
            new_data.append(update_stream_data(item))
        return new_data

    elif isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key in page_keys and isinstance(value, int):
                if value in new_pages_ids:
                    new_page = SubPropositionPage.objects.get(pk=value)
                    title_list = [new_page.title, new_page.title + f" {TITLE_SUFFIX}"]
                    slug_list = [new_page.slug, new_page.slug + SLUG_SUFFIX]
                    old_page_instance = SubServicePage.objects.filter(
                        title__in=title_list,
                        slug__in=slug_list,
                    ).first()
                    if old_page_instance:
                        new_data[key] = old_page_instance.pk
                else:
                    new_data[key] = value
            elif key == "value" and isinstance(value, str):
                # Use regex to search and replace old page IDs with new page IDs
                pattern = r'<a id="(\d+)" linktype="page">'
                new_value = re.sub(
                    pattern, lambda match: replace_link(match, new_pages_ids), value
                )
                new_data[key] = new_value
            else:
                new_data[key] = update_stream_data(value)
        return new_data

    else:
        return data


def update_page_links():
    pages = Page.objects.not_type(SubPropositionPage).specific()
    all_page_fields = [page._meta.get_fields() for page in pages]
    flattened_page_fields = list(chain.from_iterable(all_page_fields))
    unique_page_fields = set(flattened_page_fields)
    streamfield_names = [
        field.name for field in unique_page_fields if is_streamfield(field)
    ]
    unique_streamfield_names = set(streamfield_names)

    # release memory
    del all_page_fields
    del flattened_page_fields
    del unique_page_fields
    del streamfield_names

    # we exclude some pages because they somehow trigger a segmentation fault
    # when running this command
    titles_to_exclude = [
        "An Extra 3 Million Organic Clicks a Month for the NHS Website",  # WorkPage
        "Raising millions for Islamic Relief UK during Ramadan",  # WorkPage
    ]
    report_data = [
        [
            "page id",
            "Title",
            "Streamfield name",
            "Error",
        ],
    ]
    for page in pages.filter(title__in=titles_to_exclude):
        report_data.append(
            [
                page.id,
                page.title,
                "Unknown",
                "Page excluded from migration due to segmentation fault",
            ]
        )

    for page in pages.exclude(title__in=titles_to_exclude):
        # Iterate through each streamfield name
        for streamfield_name in unique_streamfield_names:
            # Check if the page has the current streamfield
            if hasattr(page, streamfield_name):
                field = getattr(page, streamfield_name)
                try:
                    stream_data = field.get_prep_value()
                    new_stream_data = update_stream_data(stream_data)
                    updated_data = StreamValue(
                        field.stream_block,
                        new_stream_data,
                        is_lazy=True,
                    )
                    if stream_data != updated_data:
                        setattr(page, streamfield_name, updated_data)

                        revision = page.save_revision()
                        if page.live:
                            revision.publish()
                        page.save()
                except AttributeError as attr_err:
                    logger.exception(
                        f"Error updating {streamfield_name} "
                        f"on page {page.id} ({page.title}): {attr_err}"
                    )
                except ValidationError as val_err:
                    logger.exception(
                        f"Error updating {streamfield_name} "
                        f"on page {page.id} ({page.title}): {val_err}"
                    )
                    report_data.append(
                        [
                            page.id,
                            page.title,
                            streamfield_name,
                            val_err,
                        ]
                    )
                # release memory
                finally:
                    if "stream_data" in locals():
                        del stream_data
                    if "new_stream_data" in locals():
                        del new_stream_data
                    if "updated_data" in locals():
                        del updated_data
                    if "revision" in locals():
                        del revision
                    if "field" in locals():
                        del field

    return report_data


def update_rich_text_links():
    pages = Page.objects.not_type(SubPropositionPage).specific()
    all_page_fields = [page._meta.get_fields() for page in pages]
    flattened_page_fields = list(chain.from_iterable(all_page_fields))
    unique_page_fields = set(flattened_page_fields)
    rich_text_names = [
        field.name
        for field in unique_page_fields
        if field.__class__.__name__ == "RichTextField"
    ]
    unique_rich_text_names = set(rich_text_names)

    # release memory
    del all_page_fields
    del flattened_page_fields
    del unique_page_fields
    del rich_text_names

    new_pages_ids = SubPropositionPage.objects.all().values_list("pk", flat=True)

    for page in pages:
        # Iterate through each rich text name
        for rich_text_name in unique_rich_text_names:
            # Check if the page has the current rich text field
            if hasattr(page, rich_text_name):
                rich_text_field = getattr(page, rich_text_name)
                changes_made = False
                for page_id in new_pages_ids:
                    if f'<a id="{page_id}"' in rich_text_field:
                        new_page = SubPropositionPage.objects.get(pk=page_id)
                        title_list = [
                            new_page.title,
                            new_page.title + f" {TITLE_SUFFIX}",
                        ]
                        slug_list = [new_page.slug, new_page.slug + SLUG_SUFFIX]
                        old_page = SubServicePage.objects.filter(
                            title__in=title_list,
                            slug__in=slug_list,
                        ).first()
                        if old_page:
                            new_rich_text_value = rich_text_field.replace(
                                str(f'<a id="{page_id}"'), str(f'<a id="{old_page.id}"')
                            )
                            setattr(page, rich_text_name, new_rich_text_value)
                            changes_made = True

                if changes_made:
                    revision = page.save_revision()
                    if page.live:
                        revision.publish()
                    page.save()

                # release memory
                if "rich_text_field" in locals():
                    del rich_text_field


class Command(BaseCommand):
    help = "Undo migration of SubServicePages to PropositionPages"

    def show_status(self, message):
        """
        Prints a message to the console.
        This is helpful for debugging.

        Args:
            message (str): The message to be printed.

        Returns:
            None
        """
        self.stdout.write(self.style.NOTICE(message))

    def handle(self, *args, **options):
        """
        Approach:
        - Check if there are any migration records. If not, exit.
        - For each migration record:
            - Delete the corresponding SubPropositionPage
            - Revert the SubServicePage back to its 'original' state
            - Revert changes to StreamField & RichTextField links to avoid 404 errors
            - Delete the migration record

        Caveats:
        - We have no control on changes made to the page after the migration.
        """
        # if records exist, undo the migration, otherwise, exit
        if not MigrationRecord.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No migration records found. If you want to create migrations, run:"
                    "\n\n./manage.py migrate_subservicepages"
                )
            )
            return

        start_time = time.time()

        num_migration_records_deleted = 0
        num_subproposition_pages_deleted = 0
        num_subservice_pages_reverted = 0

        for migration_record in MigrationRecord.objects.all():
            subservice_page = migration_record.subservice_page
            subproposition_page = migration_record.subproposition_page

            if subservice_page and subproposition_page:
                # Delete the corresponding SubPropositionPage
                self.show_status(f"Now deleting {subproposition_page}...")
                subproposition_page.delete()
                num_subproposition_pages_deleted += 1

                # Revert the SubServicePage back to its 'original' state
                subservice_page.title = subservice_page.title.rsplit(TITLE_SUFFIX, 1)[0]
                subservice_page.slug = subservice_page.slug.rsplit(SLUG_SUFFIX, 1)[0]
                revision = subservice_page.save_revision()
                # If the page was live before the migration, publish it
                if (
                    migration_record.subservice_page_was_live
                    and not subservice_page.live
                ):
                    revision.publish()
                    subservice_page.live = True

                subservice_page.save()
                num_subservice_pages_reverted += 1

                # Delete the migration record
                self.show_status(f"Now deleting {migration_record}...")
                migration_record.delete()
                num_migration_records_deleted += 1

        # Update links
        self.show_status("Now reverting changes to links in richtext fields ...")
        update_rich_text_links()
        self.show_status("Now reverting changes to links in streamfields ...")
        pages_to_manually_check = update_page_links()

        if (n := num_migration_records_deleted) > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "{} migration record{} {} been deleted successfully.".format(
                        n, pluralize(n), pluralize(n, "has,have")
                    )
                )
            )
            n2 = num_subproposition_pages_deleted
            self.stdout.write(
                self.style.SUCCESS(
                    "{} SubPropositionPage{} {} been deleted successfully.".format(
                        n2, pluralize(n2), pluralize(n2, "has,have")
                    )
                )
            )
            n3 = num_subservice_pages_reverted
            self.stdout.write(
                self.style.SUCCESS(
                    "{} SubServicePage{} {} been successfully reverted to their previous state".format(
                        n3, pluralize(n3), pluralize(n3, "has,have")
                    )
                )
            )

            if len(pages_to_manually_check) > 1:
                self.show_status(
                    "The following pages require manual checking of links to avoid 404s:"
                )
                for index, row in enumerate(pages_to_manually_check):
                    if index == 0:
                        continue  # Skip the header row
                    (
                        page_id,
                        page_title,
                        streamfield_name,
                        error,
                    ) = row
                    self.stdout.write(f"{index}.  {page_title}")
                    self.stdout.write("-" * 60)
                    self.stdout.write(f"    Page id: {page_id}")
                    self.stdout.write(f"    Streamfield name: {streamfield_name}")
                    self.stdout.write(f"    Error: {error}")

        else:
            self.stdout.write(self.style.NOTICE("No changes made."))

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        self.stdout.write("-" * 60)
        self.show_status(f"Execution time: {int(minutes)} min, {int(seconds)} sec.")
        self.stdout.write("-" * 60)
