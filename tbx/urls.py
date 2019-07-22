from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_headers

from graphene_django.views import GraphQLView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.core.models import Page
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail_review import urls as wagtailreview_urls

from tbx.core import urls as torchbox_urls
from tbx.core.utils.cache import get_default_cache_control_decorator
from tbx.core.views import robots

private_urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
] + decorate_urlpatterns([
    path('documents/', include(wagtaildocs_urls)),
], never_cache)

urlpatterns = [
    path('sitemap.xml', sitemap),
    path('robots.txt', robots),
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
        path('test404/', TemplateView.as_view(template_name='404.html')),
        path('test500/', TemplateView.as_view(template_name='500.html')),
    ]


urlpatterns += [
    path('review/', include(wagtailreview_urls)),
    path('', include(torchbox_urls)),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', lambda request: HttpResponseNotFound(), name='home'),
]


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
urlpatterns = private_urlpatterns + urlpatterns + decorate_urlpatterns([
    # Wagtail paths have to be enabled for the administration interface to work
    # properly. This allows them to be visited only by the logged-in users to
    # avoid the public accessing it.
    path('wagtail/', include(wagtail_urls))
], login_required)
