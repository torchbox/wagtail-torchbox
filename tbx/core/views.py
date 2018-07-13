from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static

import requests


def error404(request):
    if '/play/' in request.path:
        return render(request, 'play_404.html', {'play_404': True}, status=404)
    else:
        return render(request, '404.html', status=404)


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
        "Disallow: /search/",
        "Allow: /",
    ])
    return HttpResponse(content, content_type='text/plain')
