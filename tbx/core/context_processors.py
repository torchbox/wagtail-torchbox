from django.conf import settings
from django.core.cache import cache

from tbx.core.api import PeopleHRFeed
from tbx.core.models import JobIndexPage


def fb_app_id(request):
    return {
        "FB_APP_ID": settings.FB_APP_ID,
    }


def peoplehr_jobs_count(request):
    """
    Add the number of open jobs to the context
    """
    CACHE_KEY = "job_count"
    CACHE_TIMEOUT = 60 * 60 * 6

    job_count = cache.get(CACHE_KEY)

    if not job_count:
        job_index = JobIndexPage.objects.first()
        if job_index:
            peoplehr_feed = PeopleHRFeed()
            job_count = peoplehr_feed.get_job_count(job_index.jobs_xml_feed)
        else:
            job_count = 0
        cache.set(CACHE_KEY, job_count, CACHE_TIMEOUT)

    return {"job_count": job_count}


def global_vars(request):
    return {
        "GOOGLE_TAG_MANAGER_ID": getattr(settings, "GOOGLE_TAG_MANAGER_ID", None),
    }
