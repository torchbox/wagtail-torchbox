from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.core.models import Page
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail_review import urls as wagtailreview_urls

from tbx.core import urls as torchbox_urls
from tbx.core.utils.cache import get_default_cache_control_decorator
from tbx.core.views import favicon, robots

private_urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
] + decorate_urlpatterns([
    url(r'^documents/', include(wagtaildocs_urls)),
], never_cache)

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap),
    url(r'^favicon.ico$', favicon),
    url(r'^robots.txt$', robots),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        url(r'^test404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^test500/$', TemplateView.as_view(template_name='500.html')),
    ]


urlpatterns += [
    url(r'^review/', include(wagtailreview_urls)),
    url(r'', include(torchbox_urls)),
]

handler404 = 'tbx.core.views.error404'


# Set public URLs to use public cache.
urlpatterns = decorate_urlpatterns(urlpatterns,
                                   get_default_cache_control_decorator())

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers('Cookie', 'X-Requested-With', 'X-Forwarded-Proto',
                    'Accept-Encoding')
)

Page.serve = get_default_cache_control_decorator()(Page.serve)

# Join private and public URLs.
urlpatterns = private_urlpatterns + urlpatterns + [
    # Add Wagtail URLs at the end.
    # Wagtail cache-control is set on the page models's serve methods.
    url(r'', include(wagtail_urls)),
]
