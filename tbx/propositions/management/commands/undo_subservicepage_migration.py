import logging
import time

from django.core.management import BaseCommand
from django.db.models import QuerySet
from django.template.defaultfilters import pluralize

from tbx.propositions.management.commands.migrate_subservicepages import (
    update_page_links,
    update_rich_text_links,
)
from tbx.propositions.models import SubPropositionPage
from tbx.propositions.models import (
    SubServicePageToSubPropositionPageMigration as MigrationRecord,
)
from tbx.services.constants import (
    DEPRECATED_SLUG_SUFFIX,
    DEPRECATED_TITLE_SUFFIX,
)
from tbx.services.models import SubServicePage

logger = logging.getLogger(__name__)


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
            - Alter the corresponding SubPropositionPage's title & slug to avoid clashes.
              If the SubPropositionPage is live, unpublish it
            - Revert the SubServicePage back to its 'original' state
        - Revert changes to StreamField & RichTextField links to avoid 404 errors
        - Delete the migration records
        - Delete the SubPropositionPages

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

        num_subservice_pages_reverted = 0

        for migration_record in MigrationRecord.objects.all():
            subservice_page = migration_record.subservice_page
            subproposition_page = migration_record.subproposition_page

            if subservice_page and subproposition_page:
                # to avoid clashes with the SubServicePage we're about to revert,
                # change the SubPropositionPage's title & slug, and unpublish if live
                self.show_status(
                    f"Now altering title & slug for {subproposition_page}..."
                )
                subproposition_page.title += f" {DEPRECATED_TITLE_SUFFIX}"
                # to avoid ValidationError:
                # {'slug': ["The slug '***--deprecated' is already in use within the parent page at ...]}
                subproposition_page.slug += 2 * DEPRECATED_SLUG_SUFFIX
                subproposition_page.save_revision()
                if subproposition_page.live:
                    self.show_status(f"Now unpublishing {subproposition_page}...")
                    subproposition_page.unpublish()
                subproposition_page.save()

                # Revert the SubServicePage back to its 'original' state
                subservice_page.title = subservice_page.title.rsplit(
                    DEPRECATED_TITLE_SUFFIX, 1
                )[0]
                subservice_page.slug = subservice_page.slug.rsplit(
                    DEPRECATED_SLUG_SUFFIX, 1
                )[0]
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

        # Update links
        self.show_status("Now reverting changes to links in richtext fields ...")
        update_rich_text_links(SubPropositionPage, SubServicePage, reverse=True)
        self.show_status("Now reverting changes to links in streamfields ...")
        pages_to_manually_check = update_page_links(
            SubPropositionPage, SubServicePage, reverse=True
        )

        # Delete the migration records
        self.show_status("Now deleting Migration Records ...")
        num_migration_records_deleted, _ = MigrationRecord.objects.all().delete()

        # Delete the SubPropositionPages
        self.show_status("Now deleting Subproposition Pages ...")
        _, objects_deleted = (
            QuerySet(model=SubPropositionPage)
            .filter(title__endswith=DEPRECATED_TITLE_SUFFIX)
            .delete()
        )
        num_subproposition_pages_deleted = objects_deleted.get(
            "propositions.SubPropositionPage"
        )

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
