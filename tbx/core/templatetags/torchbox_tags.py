from django import template
from django.conf import settings

from tbx.blog.models import BlogPage
from tbx.core.models import Advert, JobIndexPage, MainMenu
from tbx.core.utils import roundrobin
from tbx.people.models import PersonPage
from tbx.work.models import WorkPage

register = template.Library()


@register.simple_tag
def get_popular_tags(model):
    return model.get_popular_tags()


# settings value
@register.simple_tag
def get_googe_maps_key():
    return getattr(settings, "GOOGLE_MAPS_KEY", "")


@register.simple_tag
def get_next_sibling_by_order(page):
    sibling = page.get_next_siblings().live().first()

    if sibling:
        return sibling.specific


@register.simple_tag
def get_prev_sibling_by_order(page):
    sibling = page.get_prev_siblings().live().first()

    if sibling:
        return sibling.specific


@register.simple_tag
def get_next_sibling_blog(page):
    sibling = (
        BlogPage.objects.filter(date__lt=page.date).order_by("-date").live().first()
    )
    if sibling:
        return sibling.specific


@register.simple_tag
def get_prev_sibling_blog(page):
    sibling = (
        BlogPage.objects.filter(date__gt=page.date).order_by("-date").live().last()
    )
    if sibling:
        return sibling.specific


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context["request"].site.root_page


@register.filter
def content_type(value):
    return value.__class__.__name__.lower()


@register.simple_tag
def main_menu():
    return MainMenu.objects.first()


# Person feed for home page
@register.inclusion_tag(
    "torchbox/tags/homepage_people_listing.html", takes_context=True
)
def homepage_people_listing(context, count=3):
    people = PersonPage.objects.filter(live=True).order_by("?")[:count]
    return {
        "people": people,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


# Blog feed for home page
@register.inclusion_tag("torchbox/tags/homepage_blog_listing.html", takes_context=True)
def homepage_blog_listing(context, count=6):
    blog_posts = BlogPage.objects.live().in_menu().order_by("-date")[:count]
    return {
        "blog_posts": blog_posts,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


# Work feed for home page
@register.inclusion_tag("torchbox/tags/homepage_work_listing.html", takes_context=True)
def homepage_work_listing(context, count=3):
    work = WorkPage.objects.filter(live=True)[:count]
    return {
        "work": work,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


# Jobs feed for home page
@register.inclusion_tag("torchbox/tags/homepage_job_listing.html", takes_context=True)
def homepage_job_listing(context, count=3, intro_text=None):
    # Assume there is only one job index page
    jobindex = JobIndexPage.objects.filter(live=True).first()
    if jobindex:
        jobs = jobindex.job.all()
        if count:
            jobs = jobs[:count]
    else:
        jobs = []
    jobintro = intro_text or jobindex and jobindex.listing_intro
    return {
        "jobintro": jobintro,
        "jobindex": jobindex,
        "jobs": jobs,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


# Advert snippets
@register.inclusion_tag("torchbox/tags/adverts.html", takes_context=True)
def adverts(context):
    return {
        "adverts": Advert.objects.all(),
        "request": context["request"],
    }


# blog posts by team member
@register.inclusion_tag("torchbox/tags/person_blog_listing.html", takes_context=True)
def person_blog_post_listing(context, calling_page=None):
    posts = (
        BlogPage.objects.filter(authors__author__person_page_id=calling_page.id)
        .live()
        .order_by("-date")
    )
    return {
        "posts": posts,
        "calling_page": calling_page,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


@register.inclusion_tag("torchbox/tags/work_and_blog_listing.html", takes_context=True)
def work_and_blog_listing(context, count=10):
    """
    An interleaved list of work and blog items.
    """
    blog_posts = BlogPage.objects.filter(live=True)
    works = WorkPage.objects.filter(live=True)

    # If (remaining) count is odd, blog_count = work_count + 1
    blog_count = (count + 1) / 2
    work_count = count / 2

    blog_posts = blog_posts.order_by("-date")[:blog_count]
    works = works.order_by("-pk")[:work_count]

    return {
        "items": list(roundrobin(blog_posts, works)),
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


# Format times e.g. on event page
@register.filter
def time_display(time):
    # Get hour and minute from time object
    hour = time.hour
    minute = time.minute

    # Convert to 12 hour format
    if hour >= 12:
        pm = True
        hour -= 12
    else:
        pm = False
    if hour == 0:
        hour = 12

    # Hour string
    hour_string = str(hour)

    # Minute string
    if minute != 0:
        minute_string = "." + str(minute)
    else:
        minute_string = ""

    # PM string
    if pm:
        pm_string = "pm"
    else:
        pm_string = "am"

    # Join and return
    return "".join([hour_string, minute_string, pm_string])
