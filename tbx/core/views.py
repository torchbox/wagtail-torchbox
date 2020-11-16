from django.conf import settings
from django.http import HttpResponse

import requests


def newsletter_subsribe(request):
    if request.is_ajax() and request.GET.get("email"):
        requests.post(
            "https://us10.api.mailchimp.com/2.0/lists/subscribe",
            json={
                "apikey": settings.MAILCHIMP_KEY,
                "id": settings.MAILCHIMP_MAILING_LIST_ID,
                "email": {"email": request.GET.get("email")},
            },
        )
    return HttpResponse()


def robots(request):
    content = "\n".join(
        [
            "User-Agent: *",
            "Disallow: /admin/",
            "Disallow: /django-admin/",
            "Disallow: /wagtail/",
        ]
    )
    return HttpResponse(content, content_type="text/plain")
