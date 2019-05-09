from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static

import requests


def newsletter_subsribe(request):
    if request.is_ajax() and request.GET.get('email'):
        requests.post(
            "https://us10.api.mailchimp.com/2.0/lists/subscribe",
            json={'apikey': settings.MAILCHIMP_KEY,
                  'id': settings.MAILCHIMP_MAILING_LIST_ID,
                  'email': {'email': request.GET.get('email')}}
        )
    return HttpResponse()


def favicon(request):
    try:
        favicon_path = settings.FAVICON_STATIC_PATH
    except AttributeError:
        raise Http404
    return redirect(static(favicon_path), permanent=True)


def robots(request):
    content = "\n".join([
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /django-admin/",
        "Disallow: /wagtail/",
    ])
    return HttpResponse(content, content_type='text/plain')
