from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.vary import vary_on_headers
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail_review import urls as wagtailreview_urls

from tbx.core import urls as torchbox_urls
from tbx.core.utils.cache import get_default_cache_control_decorator

private_urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
]

urlpatterns = [
    path('review', include(wagtailreview_urls)),
    path('', include(torchbox_urls)),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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

# Join private and public URLs.
urlpatterns = private_urlpatterns + urlpatterns
