from django.conf.urls import url

from tbx.core import views
from tbx.core.feeds import BlogFeed, PlanetDrupalFeed
from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^blog/feed/$', BlogFeed(), name='blog_feed'),
    url(r'^newsletter-subscribe', views.newsletter_subsribe),
    url(
        r'^blog/feed/planet_drupal/$',
        PlanetDrupalFeed(),
        name='planet_drupal_feed'
    ),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
]
