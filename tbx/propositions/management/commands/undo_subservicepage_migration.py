from django.core.management import BaseCommand
from django.template.defaultfilters import pluralize

from tbx.propositions.constants import SLUG_SUFFIX, TITLE_SUFFIX
from tbx.propositions.models import (
    SubServicePageToSubPropositionPageMigration as MigrationRecord,
)


class Command(BaseCommand):
    help = "Undo migration of SubServicePages to PropositionPages"

    def handle(self, *args, **options):
        """
        Approach:
        - Check if there are any migration records. If not, exit.
        - For each migration record:
            - Delete the corresponding SubPropositionPage
            - Revert the SubServicePage back to its 'original' state
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

        num_migration_records_deleted = 0
        num_subproposition_pages_deleted = 0
        num_subservice_pages_reverted = 0

        for migration_record in MigrationRecord.objects.all():
            subservice_page = migration_record.subservice_page
            subproposition_page = migration_record.subproposition_page

            if subservice_page and subproposition_page:
                # Delete the corresponding SubPropositionPage
                # d1 = subproposition_page.delete()
                # num_subproposition_pages_deleted += d1[0]
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

                subservice_page.save()
                num_subservice_pages_reverted += 1

                # Delete the migration record
                # d2 = migration_record.delete()
                # num_migration_records_deleted += d2[0]
                num_migration_records_deleted += 1

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
        else:
            self.stdout.write(self.style.NOTICE("No changes made."))
