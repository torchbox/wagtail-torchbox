from django import template
from django.conf import settings

from torchbox.models import *

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


@register.inclusion_tag('torchbox/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    """
    Checks to see if we're in the Play section in order to return pages with
    show_in_play_menu set to True, otherwise retrieves the top menu
    items - the immediate children of the parent page. The
    has_menu_children method is necessary because the bootstrap menu
    requires a dropdown class to be applied to a parent
    """
    in_play = getattr(
        calling_page, 'show_in_play_menu', False
    ) or (
        True in [getattr(ancestor.specific, 'show_in_play_menu', False)
                 for ancestor in calling_page.get_ancestors()])
    if in_play:
        menuitems = list(StandardPage.objects.filter(
            live=True,
            show_in_play_menu=True
        ))
        menuitems.extend(PersonIndexPage.objects.filter(
            live=True,
            show_in_play_menu=True
        ))
        menuitems.extend(WorkIndexPage.objects.filter(
            live=True,
            show_in_play_menu=True
        ))
        for menuitem in menuitems:
            menuitem.is_active = False
            if menuitem == calling_page:
                menuitem.is_active = True
        return {
            'menuitems': menuitems,
            'calling_page': calling_page,
            # required by the pageurl tag that we want to use within this template
            'request': context['request'],
        }
    else:
        pass

    menuitems = parent.get_children().filter(
        live=True,
        show_in_menus=True
    )
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.is_active = False
        if context['request'].path.startswith(menuitem.url):
            menuitem.is_active = True

    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
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
    people = PersonPage.objects.filter(live=True).order_by('?')
    return {
        'people': people[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Blog feed for home page
@register.inclusion_tag('torchbox/tags/homepage_blog_listing.html', takes_context=True)
def homepage_blog_listing(context, count=3):
    blogs = BlogPage.objects.filter(live=True).order_by('-date')
    return {
        'blogs': blogs[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Work feed for home page
@register.inclusion_tag('torchbox/tags/homepage_work_listing.html', takes_context=True)
def homepage_work_listing(context, count=3):
    work = WorkPage.objects.filter(live=True).order_by('?')
    return {
        'work': work[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

# Jobs feed for home page
@register.inclusion_tag('torchbox/tags/homepage_job_listing.html', takes_context=True)
def homepage_job_listing(context, count=3):
    #assume there is only one job index page
    jobindex = JobIndexPage.objects.filter(live=True)[0]
    jobs = jobindex.jobs
    return {
        'jobs': jobs[:count],
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
