from django import template
from django.conf import settings

from torchbox.models import *
from torchbox.utils import *

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


def has_menu_children(page):
    if page.get_children().filter(live=True, show_in_menus=True):
        return True
    else:
        return False


@register.filter
def content_type(value):
    return value.__class__.__name__.lower()


@register.filter
def in_play(page):
    return is_in_play(page)


@register.inclusion_tag('torchbox/tags/top_menu.html', takes_context=True)
def top_menu(context, calling_page=None):
    """
    Checks to see if we're in the Play section in order to return pages with
    show_in_play_menu set to True, otherwise retrieves the top menu
    items - the immediate children of the site root. Also detects 404s in the
    Play section.
    """
    if (calling_page and in_play(calling_page)) or context.get('play_404', False):
        play_models = [
            StandardPage,
            PersonIndexPage,
            WorkIndexPage,
            BlogIndexPage
        ]
        menuitems = chain(*[
            model.objects.filter(
                live=True,
                show_in_play_menu=True,
                show_in_menus=False
            ) for model in play_models
        ])
    else:
        menuitems = get_site_root(context).get_children().filter(
            live=True,
            show_in_menus=True
        )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
        'play_404': context.get('play_404', False)
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('torchbox/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.filter(
        live=True,
        show_in_menus=True
    )
    return {
        'calling_page': calling_page,
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the secondary links - only the children of the current page, NOT the siblings, and only when not viewing the homepage
@register.inclusion_tag('torchbox/tags/secondary_menu.html', takes_context=True)
def secondary_menu(context, calling_page=None):
    menuitems = []
    if calling_page and calling_page.id != get_site_root(context).id:
        menuitems = calling_page.get_children().filter(
            live=True,
            show_in_menus=True
        )

        # If no children found and calling page parent isn't the root, get the parent's children
        if len(menuitems) == 0 and calling_page.get_parent().id != get_site_root(context).id:
            menuitems = calling_page.get_parent().get_children().filter(
                live=True,
                show_in_menus=True
            )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


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
def homepage_blog_listing(context, count=3):
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
def homepage_job_listing(context, count=3):
    # Assume there is only one job index page
    jobindex = JobIndexPage.objects.filter(live=True)[0]
    jobs = jobindex.jobs
    if count:
        jobs = jobs[:count]
    return {
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
def work_and_blog_listing(context, count=6):
    """
    An interleaved list of work and blog items.
    """
    # Exercise for the reader: what should this do if count is an odd number?
    count /= 2
    blog_posts = play_filter(BlogPage.objects.filter(live=True).order_by('-date'), count)
    works = play_filter(WorkPage.objects.filter(live=True).order_by('-pk'), count)
    blog_items = [template.loader.render_to_string(
        "torchbox/tags/blog_list_item.html",
        {'post': post,
         'request': context['request']}
    ) for post in blog_posts]
    work_items = [template.loader.render_to_string(
        "torchbox/tags/work_list_item.html",
        {'work': work,
         'request': context['request']}
    ) for work in works]
    return {
        'items': list(roundrobin(blog_items, work_items)),
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
