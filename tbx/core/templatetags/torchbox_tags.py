from django import template
from django.conf import settings

from tbx.core.models import *
from tbx.core.utils import *

register = template.Library()


@register.assignment_tag
def get_popular_tags(model):
    return model.get_popular_tags()


# settings value
@register.assignment_tag
def get_googe_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_KEY', "")


@register.assignment_tag
def get_next_sibling_by_order(page):
    sibling = page.get_next_siblings().live().first()

    if sibling:
        return sibling.specific


@register.assignment_tag
def get_prev_sibling_by_order(page):
    sibling = page.get_prev_siblings().live().first()

    if sibling:
        return sibling.specific


@register.assignment_tag
def get_next_sibling_blog(page):
    sibling = BlogPage.objects.filter(date__lt=page.date).order_by('-date').live().first()
    if sibling:
        return sibling.specific


@register.assignment_tag
def get_prev_sibling_blog(page):
    sibling = BlogPage.objects.filter(date__gt=page.date).order_by('-date').live().last()
    if sibling:
        return sibling.specific


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


@register.filter
def content_type(value):
    # marketing landing page should behave like the homepage in templates
    if value.__class__.__name__.lower() == 'marketinglandingpage':
        return 'homepage'
    return value.__class__.__name__.lower()


@register.filter
def in_play(page):
    return is_in_play(page)


@register.simple_tag
def main_menu():
    return MainMenu.objects.first()


# Person feed for home page
@register.inclusion_tag('torchbox/tags/homepage_people_listing.html', takes_context=True)
def homepage_people_listing(context, count=3):
    people = play_filter(PersonPage.objects.filter(live=True).order_by('?'),
                         count)
    return {
        'people': people,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Blog feed for home page
@register.inclusion_tag('torchbox/tags/homepage_blog_listing.html', takes_context=True)
def homepage_blog_listing(context, count=6):
    blog_posts = play_filter(BlogPage.objects.filter(live=True).order_by('-date'), count)
    return {
        'blog_posts': blog_posts,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Work feed for home page
@register.inclusion_tag('torchbox/tags/homepage_work_listing.html', takes_context=True)
def homepage_work_listing(context, count=3):
    work = play_filter(WorkPage.objects.filter(live=True),
                       count)
    return {
        'work': work,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Jobs feed for home page
@register.inclusion_tag('torchbox/tags/homepage_job_listing.html', takes_context=True)
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
        'jobintro': jobintro,
        'jobindex': jobindex,
        'jobs': jobs,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Advert snippets
@register.inclusion_tag('torchbox/tags/adverts.html', takes_context=True)
def adverts(context):
    return {
        'adverts': Advert.objects.all(),
        'request': context['request'],
    }


# blog posts by team member
@register.inclusion_tag('torchbox/tags/person_blog_listing.html', takes_context=True)
def person_blog_post_listing(context, calling_page=None):
    posts = play_filter(BlogPage.objects.filter(related_author__author=calling_page.id).live().order_by('-date'))
    return {
        'posts': posts,
        'calling_page': calling_page,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('torchbox/tags/work_and_blog_listing.html', takes_context=True)
def work_and_blog_listing(context, count=10, marketing=False):
    """
    An interleaved list of work and blog items.
    """
    blog_posts = BlogPage.objects.filter(live=True)
    works = WorkPage.objects.filter(live=True)
    if marketing:
        featured_items = context['page'].featured_items.all()

        # Reduce remaining item count accordingly, but not to below 0.
        count = max(count - featured_items.count(), 0)

        # For marketing landing page return only posts and works
        # tagged with "digital_marketing"
        featured_items_ids = featured_items.values_list('related_page_id', flat=True)
        filter_tag = "digital_marketing"
        blog_posts = blog_posts.filter(tags__tag__slug=filter_tag).exclude(pk__in=featured_items_ids)
        works = works.filter(tags__tag__slug=filter_tag).exclude(pk__in=featured_items_ids)
    else:
        # For normal case, do not display "marketing_only" posts and works
        blog_posts = blog_posts.exclude(marketing_only=True)
        works = works.exclude(marketing_only=True)
        featured_items = []
    
    # If (remaining) count is odd, blog_count = work_count + 1
    blog_count = (count + 1) / 2
    work_count = count / 2

    blog_posts = play_filter(blog_posts.order_by('-date'), blog_count)
    works = play_filter(works.order_by('-pk'), work_count)

    return {
        'featured_items': featured_items,
        'items': list(roundrobin(blog_posts, works)),
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
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
