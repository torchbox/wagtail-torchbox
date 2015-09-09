from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.conf import settings
import os.path

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

from tbx.core import urls as torchbox_urls

admin.autodiscover()


# Signal handlers
from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as wagtailsearch_register_signal_handlers
wagtailsearch_register_signal_handlers()


urlpatterns = patterns('',
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_frontend_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),


    url(r'^test404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^test500/$', TemplateView.as_view(template_name="500.html")),

    url(r'', include(torchbox_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include(wagtail_urls)),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()  # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += patterns('',
        (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'torchbox.com/images/favicon.ico'))
    )

handler404 = 'tbx.core.views.error404'
