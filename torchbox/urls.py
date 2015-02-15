from django.conf.urls import url

from torchbox.models import BlogFeed

urlpatterns = [
    url(r'^blog/feed/$', BlogFeed())
]
