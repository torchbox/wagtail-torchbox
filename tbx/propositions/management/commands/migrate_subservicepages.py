import csv
import logging
import re
import tempfile
import time
from io import StringIO
from itertools import chain

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.template.defaultfilters import pluralize
from django.utils import timezone

from tbx.propositions.models import SubPropositionPage
from tbx.propositions.models import (
    SubServicePageToSubPropositionPageMigration as MigrationRecord,
)
from tbx.services.constants import (
    DEPRECATED_SLUG_SUFFIX,
    DEPRECATED_TITLE_SUFFIX,
)
from tbx.services.models import SubServicePage
from wagtail.blocks import StreamValue
from wagtail.fields import StreamField
from wagtail.models import Page, Site

logger = logging.getLogger(__name__)

today = timezone.now()
site_url = Site.objects.filter(is_default_site=True).first().root_url
message = f"""
Hello there,

This is an automated email containing details of a
migration operation performed on {site_url} on
{today.strftime("%d %B %Y at %H:%M:%S %Z")}

Please see the attached report(s) of the migration
from SubServicePages to PropositionPages.

Best,

» {site_url}
"""

STREAMFIELD_PROCESSING_ERRORS = [
    [
        "№",
        "Operation",
        "Block",
        "SubServicePage",
        "SubPropositionPage",
        "Error",
    ]
]

# -----------------------------------------------------------------------------
# 0. Helper functions
# -----------------------------------------------------------------------------


def add_stream_block_to_content(page, block_type, block_value, save_revision=True):
    """
    Appends a new child block of the specified type and value
    to the provided page's `content` StreamField.

    Args:
        page (wagtail.models.Page): The page object to which the
        child block will be added.
        block_type (str): The type of the child block to be added
        (e.g., "key_points", "testimonials").
        block_value (dict): The data for the child block, represented
        as a dictionary.
        save_revision (bool): Whether to save a revision of the page
        object after adding the child block. Defaults to True.

    Returns:
        None
    """
    stream_data = []

    for item in page.content.get_prep_value():
        stream_data.append(item)

    stream_data.append(
        {
            "type": block_type,
            "value": block_value,
        }
    )

    page.content = StreamValue(
        page.content.stream_block,
        stream_data,
        is_lazy=True,
    )

    if save_revision:
        revision = page.save_revision()
        revision.publish()
    page.save()


def merge_blocks(page, block_type, key, val, save_revision=True):
    """
    Merges the provided block_type with the target page's
    `content` StreamField's child block of the same type.

    Args:
        page (wagtail.models.Page): The page object to which the
        child block will be added.
        block_type (str): The type of the child block we are working with
        (e.g., "key_points", "testimonials").
        key (str): The key to be used to merge the child block.
        val (str): The value to be used to merge the child block.
        save_revision (bool): Whether to save a revision of the page
        object after adding the child block. Defaults to True.

    Returns:
        Boolean: True if the block was merged, False otherwise.
    """

    # check if block_type is in the page's content StreamField
    # if not, return False, and create a new block elsewhere.
    good_to_merge = any(
        item.get("type") == block_type
        for item in page.content.blocks_by_name().stream_value.get_prep_value()
    )
    if not good_to_merge:
        return False

    stream_data = []
    for item in page.content.get_prep_value():
        if item["type"] == block_type:
            data = item["value"].get(key, [])
            data.extend(val)
            stream_data.append(item)
        else:
            stream_data.append(item)

    page.content = StreamValue(
        page.content.stream_block,
        stream_data,
        is_lazy=True,
    )
    if save_revision:
        revision = page.save_revision()
        revision.publish()

    page.save()

    return True


def is_streamfield(field):
    return isinstance(field, StreamField)


# -----------------------------------------------------------------------------
# 1. Create new blocks
# -----------------------------------------------------------------------------


def construct_key_points_block(source, target):
    """
    Constructs a `tbx.propositions.blocks.KeyPointsBlock` based on
    data from the provided source page and adds it to the
    target page's `content` StreamField.

    Args:
        source (services.SubServicePage): The source object containing data for
        the KeyPointsBlock.
        target (propositions.SubPropositionPage): The target object with a
        `content` StreamField where the KeyPointsBlock will be added.

    Returns:
        None
    """
    title = source.key_points_section_title
    heading_for_key_points = source.heading_for_key_points
    # each key_point has `text` and `linked_page` fields
    key_points = source.key_points.all()
    contact = source.contact
    contact_reasons = source.contact_reasons

    if title:
        data = {
            "title": title,
            "heading_for_key_points": heading_for_key_points,
            "key_points": [
                {
                    "text": key_point.text,
                    "linked_page": key_point.linked_page.pk
                    if key_point.linked_page
                    else None,
                }
                for key_point in key_points
            ],
            "contact": contact.pk if contact else None,
            "contact_reasons": contact_reasons.pk if contact_reasons else None,
        }

        add_stream_block_to_content(target, "key_points", data)


def construct_testimonials_block(source, target):
    """
    Constructs a `tbx.propositions.blocks.TestimonialsBlock` based on
    data from the provided source page and adds it to the
    target page's `content` StreamField.

    Args:
        source (services.SubServicePage): The source object containing data for
        the TestimonialsBlock.
        target (propositions.SubPropositionPage): The target object with a
        `content` StreamField where the TestimonialsBlock will be added.

    Returns:
        None
    """

    title = source.testimonials_section_title
    # each logo has an `image` field
    client_logos = source.client_logos.all()
    # each testimonial has `quote`, `name` and `role` fields
    testimonials = source.testimonials.all()

    if title:
        data = {
            "title": title,
            "client_logos": [
                {
                    "image": logo.image.pk,
                }
                for logo in client_logos
                if logo
            ],
            "testimonials": [
                {
                    "quote": testimonial.quote,
                    "name": testimonial.name,
                    "role": testimonial.role,
                }
                for testimonial in testimonials
            ],
        }

        add_stream_block_to_content(target, "testimonials", data)


def construct_processes_block(source, target):
    """
    Constructs a `tbx.propositions.blocks.ProcessesBlock` based on
    data from the provided source page and adds it to the
    target page's `content` StreamField.

    Args:
        source (services.SubServicePage): The source object containing data for
        the ProcessesBlock.
        target (propositions.SubPropositionPage): The target object with a
        `content` StreamField where the ProcessesBlock will be added.

    Returns:
        None
    """
    title = source.process_section_title
    heading_for_processes = source.heading_for_processes
    use_process_block_image = source.use_process_block_image
    processes_section_embed_url = source.processes_section_embed_url
    # each process has `title`, `description`, `external_link`, `page_link`
    # and `link_label` fields
    processes = source.processes.all()
    process_section_cta = source.process_section_cta

    if title:
        data = {
            "title": title,
            "heading_for_processes": heading_for_processes,
            "use_process_block_image": use_process_block_image,
            "processes_section_embed_url": processes_section_embed_url,
            "processes": [
                {
                    "title": process.title,
                    "description": process.description,
                    "external_link": process.external_link,
                    "page_link": process.page_link.pk if process.page_link else None,
                    "link_label": process.link_label,
                }
                for process in processes
            ],
            "process_section_cta": process_section_cta,
        }

        add_stream_block_to_content(target, "processes", data)


def construct_work_block(source, target):
    """
    Constructs a `tbx.propositions.blocks.WorkBlock` based on
    data from the provided source page and adds it to the
    target page's `content` StreamField.

    Args:
        source (services.SubServicePage): The source object containing data for
        the WorkBlock.
        target (propositions.SubPropositionPage): The target object with a
        `content` StreamField where the WorkBlock will be added.

    Returns:
        None
    """
    title = source.case_studies_section_title
    # each featured_case_study has a `case_study` field
    featured_case_studies = source.featured_case_studies.all()

    if title:
        data = {
            "title": title,
            "featured_case_studies": [
                featured_case_study.case_study.pk
                for featured_case_study in featured_case_studies
                if featured_case_study
            ],
        }

        add_stream_block_to_content(target, "work", data)


def construct_thinking_block(source, target):
    """
    Constructs a `tbx.propositions.blocks.ThinkingBlock` based on
    data from the provided source page and adds it to the
    target page's `content` StreamField.

    Args:
        source (services.SubServicePage): The source object containing data for
        the ThinkingBlock.
        target (propositions.SubPropositionPage): The target object with a
        `content` StreamField where the ThinkingBlock will be added.

    Returns:
        None
    """
    title = source.blogs_section_title
    # each featured_blog_post has a `blog_post` field
    featured_blog_posts = source.featured_blog_posts.all()

    if title:
        data = {
            "title": title,
            "featured_blog_posts": [
                featured_blog_post.blog_post.pk
                for featured_blog_post in featured_blog_posts
                if featured_blog_post
            ],
        }

        add_stream_block_to_content(target, "thinking", data)


# -----------------------------------------------------------------------------
# 2. Copy existing blocks
# -----------------------------------------------------------------------------


def copy_existing_blocks(source, target):
    """
    Copy existing blocks from SubServicePage's content StreamField to
    SubPropositionPage's content StreamField.
    """
    changes_made = False

    has_testimonials_and_clients = "testimonials" and "clients" in [
        block.block_type for block in source.content
    ]

    for block in source.content:
        # We only care about blocks with non-empty content
        if block.value:
            # Clients block
            if block.block_type == "clients" and not has_testimonials_and_clients:
                # we don't have a `clients` block on SubPropositionPage
                # therefore, we need to add this to the `testimonials` block's `client_logos` field
                data = {
                    "title": "Clients",  # this is the default title
                    "client_logos": [logo for logo in block.value if logo],
                }
                is_merged = merge_blocks(
                    target, "testimonials", "client_logos", data["client_logos"]
                )
                if not is_merged:
                    add_stream_block_to_content(target, "testimonials", data)
            # Testimonials block
            elif (
                block.block_type == "testimonials" and not has_testimonials_and_clients
            ):
                # the source & target blocks are slightly different
                # so we need to add this to the the `testimonials` block's `testimonials` field
                data = {
                    "title": "Clients",  # this is the default title
                    "client_logos": [],
                    "testimonials": [
                        {
                            "quote": testimonial.get("quote", ""),
                            "name": testimonial.get("name", ""),
                            "role": testimonial.get("role", ""),
                            "link": [
                                link.get_prep_value()
                                for link in testimonial.get("link", [])
                            ],
                        }
                        for testimonial in block.value
                    ],
                }
                is_merged = merge_blocks(
                    target, "testimonials", "testimonials", data["testimonials"]
                )
                if not is_merged:
                    add_stream_block_to_content(target, "testimonials", data)
            # Key Points Summary block
            elif block.block_type == "key_points_summary":
                # we don't have a `key_points_summary` block on SubPropositionPage
                # therefore, we need to add this to the `key_points` block's `key_points` field
                data = {
                    "title": "Services",  # this is the default title
                    "key_points": [
                        {
                            "text": key_point.text,
                            "linked_page": key_point.linked_page.pk
                            if key_point.linked_page
                            else None,
                        }
                        for key_point in block.value
                    ],
                }
                is_merged = merge_blocks(
                    target, "key_points", "key_points", data["key_points"]
                )
                if not is_merged:
                    add_stream_block_to_content(target, "key_points", data)
            else:
                # Embed + CTA block
                # CTA block
                target.content.append((block.block_type, block.value))

            changes_made = True

    if changes_made:
        target.save()

    if has_testimonials_and_clients:
        # combine the content from the source `testimonials` and `clients` blocks
        # into a single `testimonials` block on the target

        testimonials = [
            block
            for block in source.content
            if "testimonials" in block.block_type and block.value
        ]
        # the assumtion is that we only have one `testimonials` block
        assert len(testimonials) <= 1
        testimonials_block = testimonials[0] if testimonials else None

        clients = [
            block
            for block in source.content
            if "clients" in block.block_type and block.value
        ]
        # the assumtion is that we only have one `clients` block
        assert len(clients) <= 1
        clients_block = clients[0] if clients else None

        data = {
            "title": "Clients",  # this is the default title
            "client_logos": [logo for logo in clients_block.value if logo],
            "testimonials": [
                {
                    "quote": testimonial.get("quote", ""),
                    "name": testimonial.get("name", ""),
                    "role": testimonial.get("role", ""),
                    "link": [
                        link.get_prep_value() for link in testimonial.get("link", [])
                    ],
                }
                for testimonial in testimonials_block.value
            ],
        }

        good_to_merge = any(
            item.get("type") == "testimonials"
            for item in target.content.blocks_by_name().stream_value.get_prep_value()
        )
        if not good_to_merge:
            add_stream_block_to_content(target, "testimonials", data)
        else:
            merge_blocks(target, "testimonials", "testimonials", data["client_logos"])
            merge_blocks(target, "testimonials", "testimonials", data["testimonials"])


# -----------------------------------------------------------------------------
# 3. Update links
# -----------------------------------------------------------------------------


def replace_link(match, ids, reverse=False):
    """
    Replace a link to a SubServicePage with a link to a SubPropositionPage or vice versa.

    Args:
        match (re.Match): The match object returned by the regex search.
        ids (list): A list of IDs of either SubServicePages or SubPropositionPages.
        reverse (bool): If True, replace links from SubPropositionPage to SubServicePage.
    """
    page_id = int(match.group(1))
    if page_id in ids:
        page = (
            SubServicePage.objects.get(pk=page_id)
            if not reverse
            else SubPropositionPage.objects.get(pk=page_id)
        )
        if not reverse:
            title_list = [page.title.replace(f" {DEPRECATED_TITLE_SUFFIX}", "")]
            slug_list = [page.slug.replace(DEPRECATED_SLUG_SUFFIX, "")]
            target = SubPropositionPage
        else:
            title_list = [page.title, page.title + f" {DEPRECATED_TITLE_SUFFIX}"]
            slug_list = [page.slug, page.slug + DEPRECATED_SLUG_SUFFIX]
            target = SubServicePage

        target_page_instance = target.objects.filter(
            title__in=title_list,
            slug__in=slug_list,
        ).first()
        if target_page_instance:
            return f'<a id="{target_page_instance.pk}" linktype="page">'

    # Return the original match if no replacement is made
    return match.group(0)


def update_stream_data(data, source, target, reverse=False):
    """
    Recursively updates data containing links to source Pages to point to
    corresponding target Pages.

    This function is designed to process a nested data structure, such as a JSON
    object or a list, and replace links to source Pages with links to
    target Pages. It works by recursively traversing the data structure and
    performing the necessary replacements.

    Args:
        data (dict or list): The data structure containing links to source Pages
        that need to be updated.
        source (SubServicePage / SubPropositionPage class): the Page class for the links that
        we want to replace
        target (SubServicePage / SubPropositionPage class): the Page class for the desired links
        reverse (bool): If True, replace SubPropositionPage links with SubServicePage links.

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
    source_pages_ids = source.objects.all().values_list("pk", flat=True)

    if isinstance(data, list):
        target_data = []
        for item in data:
            target_data.append(
                update_stream_data(item, source, target, reverse=reverse)
            )
        return target_data

    elif isinstance(data, dict):
        target_data = {}
        for key, value in data.items():
            if key in page_keys and isinstance(value, int):
                if value in source_pages_ids:
                    source_page = source.objects.get(pk=value)
                    if reverse:
                        title_list = [
                            source_page.title,
                            source_page.title + f" {DEPRECATED_TITLE_SUFFIX}",
                        ]
                        slug_list = [
                            source_page.slug,
                            source_page.slug + DEPRECATED_SLUG_SUFFIX,
                        ]
                    else:
                        title_list = [
                            source_page.title.replace(f" {DEPRECATED_TITLE_SUFFIX}", "")
                        ]
                        slug_list = [
                            source_page.slug.replace(DEPRECATED_SLUG_SUFFIX, "")
                        ]

                    target_page_instance = target.objects.filter(
                        title__in=title_list,
                        slug__in=slug_list,
                    ).first()
                    if target_page_instance:
                        target_data[key] = target_page_instance.pk
                else:
                    target_data[key] = value
            elif key == "value" and isinstance(value, str):
                # Use regex to search and replace source page IDs with target page IDs
                pattern = r'<a id="(\d+)" linktype="page">'
                target_value = re.sub(
                    pattern,
                    lambda match: replace_link(
                        match, source_pages_ids, reverse=reverse
                    ),
                    value,
                )
                target_data[key] = target_value
            else:
                target_data[key] = update_stream_data(
                    value, source, target, reverse=reverse
                )
        return target_data

    else:
        return data


def update_page_links(source, target, reverse=False):
    pages = Page.objects.not_type(source).specific()
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
                    new_stream_data = update_stream_data(
                        stream_data, source, target, reverse=reverse
                    )
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
                    report_data.append(
                        [
                            page.id,
                            page.title,
                            streamfield_name,
                            attr_err,
                        ]
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


def update_rich_text_links(source, target, reverse=False):
    pages = Page.objects.not_type(source).specific()
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

    source_pages_ids = source.objects.all().values_list("pk", flat=True)

    for page in pages:
        # Iterate through each rich text name
        for rich_text_name in unique_rich_text_names:
            # Check if the page has the current rich text field
            if hasattr(page, rich_text_name):
                rich_text_field = getattr(page, rich_text_name)
                changes_made = False
                for page_id in source_pages_ids:
                    if f'<a id="{page_id}"' in rich_text_field:
                        source_page = source.objects.get(pk=page_id)
                        if reverse:
                            title_list = [
                                source_page.title,
                                source_page.title + f" {DEPRECATED_TITLE_SUFFIX}",
                            ]
                            slug_list = [
                                source_page.slug,
                                source_page.slug + DEPRECATED_SLUG_SUFFIX,
                            ]
                        else:
                            title_list = [
                                source_page.title.replace(
                                    f" {DEPRECATED_TITLE_SUFFIX}", ""
                                )
                            ]
                            slug_list = [
                                source_page.slug.replace(DEPRECATED_SLUG_SUFFIX, "")
                            ]

                        target_page = target.objects.filter(
                            title__in=title_list,
                            slug__in=slug_list,
                        ).first()

                        if target_page:
                            target_rich_text_value = rich_text_field.replace(
                                str(f'<a id="{page_id}"'),
                                str(f'<a id="{target_page.id}"'),
                            )
                            setattr(page, rich_text_name, target_rich_text_value)
                            changes_made = True

                if changes_made:
                    revision = page.save_revision()
                    if page.live:
                        revision.publish()
                    page.save()

                # release memory
                if "rich_text_field" in locals():
                    del rich_text_field


# -------------------------------------------------------------------------------------
# let's now wrap it all up in a Command
# -------------------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Migrate SubServicePages to PropositionPages"

    def add_arguments(self, parser):
        parser.add_argument(
            "--send-to",
            dest="recipients",
            required=False,
            nargs="*",
            help="Optional space separated list of email addresses to send the migration report to",
        )

    def notify_site_admins(self, recipients, message, attachment, *args, **kwargs):
        """
        Send a report to the site admins, listing the pages that were migrated
        """
        subject = "⚙️ Migration Report » SubServicePages to PropositionPages"
        from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
            subject,
            message,
            from_email,
            recipients,
        )
        email.attach_file(attachment)
        if extra_attachments := kwargs.get("extra_attachments"):
            for attachment in extra_attachments:
                email.attach_file(attachment)

        try:
            email.send()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully sent report to {", ".join(recipients)}'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send report: {e}"))

    def generate_report(self, report_data):
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        for row in report_data:
            csv_writer.writerow(row)

        return csv_buffer.getvalue()

    def create_temporary_csv_file(self, file_prefix, csv_data):
        # Save CSV data to a temporary file
        timestamp = today.strftime("%Y-%m-%d_%H%M%S")
        temp_file = tempfile.NamedTemporaryFile(
            prefix=f"{file_prefix}_{timestamp}",
            delete=False,
            mode="w",
            suffix=".csv",
        )
        temp_file.write(csv_data)
        temp_file.close()

        return temp_file.name

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

    def perform_streamfield_operation(self, operation, source, target):
        """
        Performs a StreamField `operation` given the `source` and `target` pages.

        If something goes wrong, we will take note of the error and carry on.

        Args:
            operation (function): The StreamField operation to be performed.
            The assumption here is that the function has two arguments: source & target.
            For instance:
                - `construct_key_points_block`
                - `construct_testimonials_block`
                - `construct_processes_block`
                - `construct_work_block`
                - `construct_thinking_block`
                - `copy_existing_blocks`
            source (services.SubServicePage): The source Page object containing data for
            the StreamField operation.
            target (propositions.SubPropositionPage): The target Page object with a
            `content` StreamField where the StreamField operation will be performed.

        Returns:
            None
        """

        action = operation.__name__.split("_")[0].capitalize()
        block = operation.__name__.replace(f"{action.lower()}_", "")
        message = f"{action}ing {block} from {source} ..."
        self.show_status(message)
        try:
            operation(source, target)
        except Exception as e:
            logger.exception(f"Error {message.replace(' ...', '')}: {e}")
            STREAMFIELD_PROCESSING_ERRORS.append(
                [
                    len(STREAMFIELD_PROCESSING_ERRORS),  # "№"
                    operation.__name__,  # "Operation"
                    block,  # "Block"
                    f"{source.pk} » {source.title}",  # "SubServicePage"
                    f"{target.pk} » {target.title}",  # "SubPropositionPage"
                    str(e),  # "Error"
                ]
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully Completed {message.replace(' ...', '')}"
                )
            )

    def handle(self, *args, **options):
        """
        Approach:

        - First, check if the migration has already been run. If it has, exit,
        providing instructions on how to undo the migration.
        - Grab all the fields we need from each SubServicePage, so that we can
        create SubPropositionPages with the same data
        - Add a suffix to the title & slug of each SubServicePage, to avoid
        clashes with the title & slug of the corresponding SubPropositionPage
        - Unpublish the SubServicePage if it's live
        - Create a SubPropositionPage with the data we grabbed earlier
        - Deal with the StreamField content
        - Add a migration record to the database, so that in future we can check
        if the migration has already been run.
        - Update StreamField & RichTextField links so that we don't have 404 errors
        - Optionally, send a report to the specified recipients, listing the
        pages that were migrated.

        Caveats:
        - All draft changes will not be transferred to the new page
        - All revisions will not be transferred to the new page
        """

        # if records exist, we've already run the migration, so we can exit.
        if MigrationRecord.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Migration has already been run. Please undo the migration first:\n"
                    "`./manage.py undo_subservicepage_migration`"
                )
            )
            return

        start_time = time.time()

        report_data = [
            [
                "№",
                "Title",
                "SubServicePage ID",
                "SubServicePage Slug",
                "SubServicePage Was Live?",
                "SubPropositionPage ID",
                "SubPropositionPage Slug",
            ]
        ]

        for count, old_page in enumerate(SubServicePage.objects.all(), start=1):
            parent = old_page.get_parent().specific
            title = old_page.title
            slug = old_page.slug
            is_live = old_page.live
            last_published_at = old_page.last_published_at

            # to avoid clashes with the new page we're about to create,
            # change the old page's title & slug, and unpublish if live
            old_page.title = f"{title} {DEPRECATED_TITLE_SUFFIX}"
            old_page.slug = f"{slug}{DEPRECATED_SLUG_SUFFIX}"

            old_page_revision = old_page.save_revision()
            if is_live:
                old_page_revision.publish()
            old_page.save()

            if is_live:
                old_page.unpublish()

            new_page = SubPropositionPage(
                title=title,
                slug=slug,
                owner=old_page.owner,
                live=is_live,
                locked=old_page.locked,
                locale=old_page.locale,
                seo_title=old_page.seo_title,
                search_description=old_page.search_description,
                show_in_menus=old_page.show_in_menus,
                social_image=getattr(old_page, "social_image", None),
                social_text=getattr(old_page, "social_text", ""),
                theme=old_page.theme,
                strapline=old_page.strapline,
                intro=old_page.intro,
                greeting_image_type=old_page.greeting_image_type,
            )

            if is_live:
                # *_published_at fields only apply to live pages
                new_page.first_published_at = old_page.first_published_at
                new_page.last_published_at = last_published_at

            if old_page.locked:
                # locked_* fields only apply to locked pages
                new_page.locked_by = old_page.locked_by
                new_page.locked_at = old_page.locked_at

            parent.add_child(instance=new_page)
            new_page.save()

            # Create a migration record
            MigrationRecord.objects.create(
                subservice_page=old_page,
                subservice_page_was_live=is_live,
                subproposition_page=new_page,
            )

            # Let's now deal with the content StreamField
            self.perform_streamfield_operation(
                construct_key_points_block, old_page, new_page
            )
            self.perform_streamfield_operation(
                construct_processes_block, old_page, new_page
            )
            self.perform_streamfield_operation(
                construct_testimonials_block, old_page, new_page
            )
            self.perform_streamfield_operation(construct_work_block, old_page, new_page)
            self.perform_streamfield_operation(
                construct_thinking_block, old_page, new_page
            )
            self.perform_streamfield_operation(copy_existing_blocks, old_page, new_page)

            # Add the page data to the report
            report_data.append(
                [
                    count,
                    title,
                    old_page.pk,
                    old_page.slug,
                    is_live,
                    new_page.pk,
                    new_page.slug,
                ]
            )

        # Update links
        self.show_status("Now updating links in richtext fields ...")
        update_rich_text_links(SubServicePage, SubPropositionPage)
        self.show_status("Now updating links in streamfields ...")
        pages_to_manually_check = update_page_links(SubServicePage, SubPropositionPage)

        total_migrations = len(report_data) - 1  # Exclude header row
        if (n := total_migrations) > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "{} migration{} {} been executed successfully.".format(
                        n, pluralize(n), pluralize(n, "has,have")
                    )
                )
            )
            if recipients := options.get("recipients"):
                csv_data = self.generate_report(report_data)
                csv_file = self.create_temporary_csv_file("migration_report", csv_data)

                extra_attachments = []

                if len(pages_to_manually_check) > 1:
                    extra_csv_data = self.generate_report(pages_to_manually_check)
                    extra_csv_file = self.create_temporary_csv_file(
                        "pages_to_manually_check_links_to_avoid_404s",
                        extra_csv_data,
                    )
                    extra_attachments.append(extra_csv_file)

                if len(STREAMFIELD_PROCESSING_ERRORS) > 1:
                    extra_csv_data = self.generate_report(STREAMFIELD_PROCESSING_ERRORS)
                    extra_csv_file = self.create_temporary_csv_file(
                        "streamfield_processing_errors", extra_csv_data
                    )
                    extra_attachments.append(extra_csv_file)

                if extra_attachments:
                    self.notify_site_admins(
                        recipients,
                        message,
                        csv_file,
                        extra_attachments=extra_attachments,
                    )
                else:
                    self.notify_site_admins(recipients, message, csv_file)
            else:
                # Display migration information, in the following format:
                """
                1.  Title
                    ------------------------------------------------------------
                    SubServicePage <ID> ⇒ SubPropositionPage <ID>
                    slugs: <Slug> ⇒ <Slug>
                    SubServicePage Was Live? <YES>
                    ------------------------------------------------------------
                2.  Title
                    ------------------------------------------------------------
                    SubServicePage <ID> ⇒ SubPropositionPage <ID>
                    slugs: <Slug> ⇒ <Slug>
                    SubServicePage Was Live? <YES>
                    ------------------------------------------------------------
                ...
                """

                for index, row in enumerate(report_data):
                    if index == 0:
                        continue  # Skip the header row

                    # Extract data
                    (
                        num,
                        title,
                        sub_service_id,
                        sub_service_slug,
                        was_live,
                        sub_proposition_id,
                        sub_proposition_slug,
                    ) = row

                    # Display Title
                    self.stdout.write(f"{num}.  {title}")
                    self.stdout.write("-" * 60)

                    # Display IDs
                    self.stdout.write(
                        f"    SubServicePage {sub_service_id} ⇒ SubPropositionPage "
                        f"{sub_proposition_id}"
                    )

                    # Display slugs
                    self.stdout.write(
                        f"    slugs: {sub_service_slug} ⇒ {sub_proposition_slug}"
                    )

                    # Display published status
                    self.stdout.write(
                        f"    SubServicePage was live? {'YES' if was_live else 'NO'}"
                    )

                    self.stdout.write("-" * 60)

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

                if len(STREAMFIELD_PROCESSING_ERRORS) > 1:
                    self.show_status(
                        "The following errors occurred while processing streamfields:"
                    )
                    for index, row in enumerate(STREAMFIELD_PROCESSING_ERRORS):
                        if index == 0:
                            continue  # Skip the header row
                        (
                            count,
                            operation,
                            block,
                            subservice_page,
                            subproposition_page,
                            error,
                        ) = row
                        self.stdout.write(f"{count}. {operation}")
                        self.stdout.write("-" * 60)
                        self.stdout.write(f"    SubServicePage: {subservice_page}")
                        self.stdout.write(
                            f"    SubPropositionPage: {subproposition_page}"
                        )
                        self.stdout.write(f"    Block: {block}")
                        self.stdout.write(f"    Error: {error}")

            # free up memory
            del report_data

        else:
            self.show_status("No migrations have been created.")

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        self.stdout.write("-" * 60)
        self.show_status(f"Execution time: {int(minutes)} min, {int(seconds)} sec.")
        self.stdout.write("-" * 60)
