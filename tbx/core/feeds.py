from datetime import datetime, time
from urllib.parse import urljoin, urlparse

from django.conf import settings
from django.contrib.syndication.views import Feed

import imghdr

from tbx.core.models import BlogPage
from tbx.core.utils import play_filter

# Main blog feed


class BlogFeed(Feed):
    title = "The Torchbox Blog"
    link = "/blog/"
    description = "The latest news and views from Torchbox on the work we do, the web and the wider world"

    def items(self):
        return play_filter(BlogPage.objects.live().order_by('-date'), 10)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.intro if item.intro else item.body

    def item_link(self, item):
        return item.get_full_url()

    def item_author_name(self, item):
        pass

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())


# Planet Drupal feed

class PlanetDrupalFeed(Feed):
    title = "The Torchbox Planet Drupal Feed"
    link = "/blog/?tag=planet-drupal"
    description = "The Torchbox Planet Drupal Feed"

    def items(self):
        return BlogPage.objects.live().filter(tags__tag__slug='planet-drupal')\
            .order_by('-date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.intro

    def item_link(self, item):
        return item.get_full_url()

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())

    def item_enclosure_url(self, item):
        if item.feed_image:
            url = item.feed_image.get_rendition('original').url
            if not urlparse(url).netloc:
                return urljoin(settings.BASE_URL, url)
            return url

    def item_enclosure_mime_type(self, item):
        if item.feed_image:
            image_format = imghdr.what(item.feed_image.get_rendition('original').file)
            return 'image/{}'.format(image_format)

    def item_enclosure_length(self, item):
        if item.feed_image:
            return item.feed_image.get_rendition('original').file.size
