from django.urls import path

from tbx.blog.feeds import BlogFeed
from tbx.core import views

urlpatterns = [
    path("blog/feed/", BlogFeed(), name="blog_feed"),
    path("newsletter-subscribe", views.newsletter_subsribe),
]
