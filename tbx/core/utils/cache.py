from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from wagtail.contrib.frontend_cache.utils import purge_url_from_cache
from wagtail.models import Site


def purge_cache_on_all_sites(path):
    if settings.DEBUG:
        return

    for site in Site.objects.all():
        purge_url_from_cache("%s%s" % (site.root_url.rstrip("/"), path))


def get_default_cache_control_kwargs():
    s_maxage = getattr(settings, "CACHE_CONTROL_S_MAXAGE", None)
    stale_while_revalidate = getattr(
        settings, "CACHE_CONTROL_STALE_WHILE_REVALIDATE", None
    )
    cache_control_kwargs = {
        "s_maxage": s_maxage,
        "stale_while_revalidate": stale_while_revalidate,
        "public": True,
    }
    return {k: v for k, v in cache_control_kwargs.items() if v is not None}


def get_default_cache_control_decorator():
    cache_control_kwargs = get_default_cache_control_kwargs()
    return cache_control(**cache_control_kwargs)


def get_default_cache_control_method_decorator(original_method):
    @method_decorator(get_default_cache_control_decorator())
    def decorated_method(self, *args, **kwargs):
        return original_method(self, *args, **kwargs)

    return decorated_method
