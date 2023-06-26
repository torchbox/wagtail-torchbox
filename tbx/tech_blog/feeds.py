from datetime import datetime, time

from django.contrib.syndication.views import Feed


class TechBlogFeed(Feed):
    def __init__(self, posts, link, title):
        self.posts = posts
        self.link = link
        self.title = title

    def __call__(self, request, *args: list, **kwargs: dict):
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def items(self):
        return self.posts

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_full_url(request=self.request)

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())
