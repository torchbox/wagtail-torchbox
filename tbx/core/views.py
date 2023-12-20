from datetime import timedelta

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

import requests


def newsletter_subsribe(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest" and request.GET.get(
        "email"
    ):
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


@method_decorator(never_cache, name="dispatch")
class SecurityView(TemplateView):
    template_name = "security.txt"
    content_type = "text/plain"

    expires = timedelta(days=7)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["security_txt"] = self.request.build_absolute_uri(self.request.path)
        context["expires"] = (
            (timezone.now() + self.expires).replace(microsecond=0).isoformat()
        )
        return context
