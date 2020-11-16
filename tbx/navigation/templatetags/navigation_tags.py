from django import template

register = template.Library()


# Primary nav snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/primary-nav.html", takes_context=True
)
def primarynav(context):
    request = context["request"]
    return {
        "primarynav": context["settings"]["navigation"][
            "NavigationSettings"
        ].primary_navigation,
        "job_count": 0,
        "request": request,
    }


# Secondary nav snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/secondary-nav.html", takes_context=True
)
def secondarynav(context):
    request = context["request"]
    return {
        "secondarynav": context["settings"]["navigation"][
            "NavigationSettings"
        ].secondary_navigation,
        "request": request,
    }


# Footer nav snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/footer-nav.html", takes_context=True
)
def footernav(context):
    request = context["request"]
    return {
        "footernav": context["settings"]["navigation"][
            "NavigationSettings"
        ].footer_navigation,
        "request": request,
    }


# Footer nav snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/sidebar.html", takes_context=True
)
def sidebar(context):
    return {
        "children": context["page"].get_children().live().public().in_menu(),
        "request": context["request"],
    }


# Footer nav snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/footerlinks.html", takes_context=True
)
def footerlinks(context):
    request = context["request"]
    return {
        "footerlinks": context["settings"]["navigation"][
            "NavigationSettings"
        ].footer_links,
        "request": request,
    }


# Footer teaser snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/teaser-list.html", takes_context=True
)
def footerteasers(context):
    request = context["request"]
    return {
        "footerteasers": context["settings"]["navigation"][
            "NavigationSettings"
        ].footer_teasers,
        "request": request,
    }
