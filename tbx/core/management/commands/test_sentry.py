from django.core.management.base import BaseCommand

from sentry_sdk import capture_exception, capture_message


class Command(BaseCommand):
    """
    Sends a message to Sentry to test if it's set up correctly

    To test locally specify the SENTRY_DSN for this command only:
    SENTRY_DSN=... ./manage.py test_sentry

    https://github.com/getsentry/sentry-python/issues/367
    """

    def handle(self, *args, **options):
        capture_message("test message")
        capture_exception(Exception("test exception"))
