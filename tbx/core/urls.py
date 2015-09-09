from django.conf.urls import url

from tbx.core.feeds import BlogFeed
from tbx.core import views

urlpatterns = [
    url(r'^blog/feed/$', BlogFeed(), name='blog_feed'),
    url(r'^newsletter-subscribe', views.newsletter_subsribe)
]
