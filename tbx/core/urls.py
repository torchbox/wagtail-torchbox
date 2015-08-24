from django.conf.urls import url

from tbx.core.feeds import BlogFeed

urlpatterns = [
    url(r'^blog/feed/$', BlogFeed(), name='blog_feed')
]
