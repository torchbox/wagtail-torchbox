from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from tbx.core import urls as torchbox_urls
from tbx.core.utils.cache import (
    get_default_cache_control_decorator,
    get_default_cache_control_method_decorator,
)
from tbx.core.views import robots
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.models import Page
from wagtail.utils.urlpatterns import decorate_urlpatterns

private_urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
] + decorate_urlpatterns([path("documents/", include(wagtaildocs_urls))], never_cache)

urlpatterns = [
    path("sitemap.xml", sitemap),
    path("robots.txt", robots),
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
        # Add views for testing 404 and 500 templates
        path(
            "test404/",
            TemplateView.as_view(template_name="patterns/pages/errors/404.html"),
        ),
        path(
            "test500/",
            TemplateView.as_view(template_name="patterns/pages/errors/500.html"),
        ),
    ]

    # Django Debug Toolbar
    if apps.is_installed("debug_toolbar"):
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


urlpatterns += [
    path("", include(torchbox_urls)),
]

# Style guide
if getattr(settings, "PATTERN_LIBRARY_ENABLED", False) and apps.is_installed(
    "pattern_library"
):
    from tbx.project_styleguide.views import example_form

    private_urlpatterns += [
        path("pattern-library/example-form/", example_form),
        path("pattern-library/", include("pattern_library.urls")),
    ]


# Set public URLs to use public cache.
urlpatterns = decorate_urlpatterns(urlpatterns, get_default_cache_control_decorator())

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers(
        "Cookie", "X-Requested-With", "X-Forwarded-Proto", "Accept-Encoding"
    ),
)

Page.serve = get_default_cache_control_method_decorator(Page.serve)

# Join private and public URLs.
urlpatterns = (
    private_urlpatterns
    + urlpatterns
    + [
        # Add Wagtail URLs at the end.
        # Wagtail cache-control is set on the page models's serve methods.
        path("", include(wagtail_urls))
    ]
)

# Error handlers
handler404 = "tbx.core.utils.views.page_not_found"
handler500 = "tbx.core.utils.views.server_error"
