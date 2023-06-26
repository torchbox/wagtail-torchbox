import imghdr
from datetime import datetime, time

from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import BlogPage

# Main blog feed


class BlogFeed(Feed):
    title = "The Torchbox Blog"
    link = "/blog/"
    description = "The latest news and views from Torchbox on the work we do, the web and the wider world"

    def items(self):
        return BlogPage.objects.live().order_by("-date")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.listing_summary

    def item_link(self, item):
        return item.get_full_url()

    def item_author_name(self, item):
        pass

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())

    def item_enclosure_url(self, item):
        if item.feed_image:
            return settings.WAGTAILADMIN_BASE_URL + item.feed_image.file.url

    def item_enclosure_mime_type(self, item):
        if item.feed_image:
            image_format = imghdr.what(item.feed_image.file)
            return "image/{}".format(image_format)

    def item_enclosure_length(self, item):
        if item.feed_image:
            return item.feed_image.file.size
