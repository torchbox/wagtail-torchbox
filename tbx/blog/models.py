from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from django.utils.decorators import method_decorator

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from tbx.core.blocks import StoryBlock
from tbx.core.models import RelatedLink, Tag
from tbx.core.utils.cache import get_default_cache_control_decorator


class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('blog.BlogIndexPage', related_name='related_links')


@method_decorator(get_default_cache_control_decorator(), name='serve')
class BlogIndexPage(Page):
    intro = models.TextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    show_in_play_menu = models.BooleanField(default=False)

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular (exclude 'planet-drupal' as this is effectively
        # the same as Drupal and only needed for the rss feed)
        popular_tags = BlogPageTagSelect.objects.all().exclude(tag__name='planet-drupal').values('tag').annotate(item_count=models.Count('tag')).order_by('-item_count')

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [Tag.objects.get(id=tag['tag']) for tag in popular_tags[:10]]

    @property
    def blog_posts(self):
        # Get list of blog pages that are descendants of this page
        # and are not marketing_only
        blog_posts = BlogPage.objects.live().in_menu().descendant_of(self).exclude(marketing_only=True)

        # Order by most recent date first
        blog_posts = blog_posts.order_by('-date', 'pk')

        return blog_posts

    def serve(self, request):
        # Get blog_posts
        blog_posts = self.blog_posts

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blog_posts = blog_posts.filter(tags__tag__slug=tag)

        # Pagination
        per_page = 12
        page = request.GET.get('page')
        paginator = Paginator(blog_posts, per_page)  # Show 10 blog_posts per page
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, "blog/includes/blog_listing.html", {
                'self': self,
                'blog_posts': blog_posts,
                'per_page': per_page,
            })
        else:
            return render(request, self.template, {
                'self': self,
                'blog_posts': blog_posts,
                'per_page': per_page,
            })

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('show_in_play_menu'),
    ]


# Blog page
class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('blog.BlogPage', related_name='related_links')


class BlogPageTagSelect(Orderable):
    page = ParentalKey('blog.BlogPage', related_name='tags')
    tag = models.ForeignKey(
        'torchbox.Tag',
        related_name='blog_page_tag_select'
    )


class BlogPageAuthor(Orderable):
    page = ParentalKey('blog.BlogPage', related_name='related_author')
    author = models.ForeignKey(
        'torchbox.PersonPage',
        null=True,
        blank=True,
        related_name='+'
    )

    panels = [
        PageChooserPanel('author'),
    ]


class BlogPage(Page):
    intro = RichTextField("Intro (used for blog index and Planet Drupal listings)", blank=True)
    body = RichTextField("body (deprecated. Use streamfield instead)", blank=True)
    colour = models.CharField(
        "Listing card colour if left blank will display image",
        choices=(
            ('orange', "Orange"),
            ('blue', "Blue"),
            ('white', "White")
        ),
        max_length=255,
        blank=True
    )
    streamfield = StreamField(StoryBlock())
    author_left = models.CharField(max_length=255, blank=True, help_text='author who has left Torchbox')
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    marketing_only = models.BooleanField(default=False, help_text='Display this blog post only on marketing landing page')

    canonical_url = models.URLField(blank=True, max_length=255)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    @property
    def blog_index(self):
        # Find blog index in ancestors
        for ancestor in reversed(self.get_ancestors()):
            if isinstance(ancestor.specific, BlogIndexPage):
                return ancestor

        # No ancestors are blog indexes,
        # just return first blog index in database
        return BlogIndexPage.objects.first()

    @property
    def has_authors(self):
        for author in self.related_author.all():
            if author.author:
                return True

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('colour'),
        InlinePanel('related_author', label="Author"),
        FieldPanel('author_left'),
        FieldPanel('date'),
        FieldPanel('intro', classname="full"),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('streamfield'),
        InlinePanel('related_links', label="Related links"),
        InlinePanel('tags', label="Tags")
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
        FieldPanel('canonical_url'),
        FieldPanel('marketing_only'),
    ]
