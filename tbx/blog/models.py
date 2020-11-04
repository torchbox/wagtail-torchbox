import math
import string

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.dispatch import receiver
from django.shortcuts import render
from django.utils.decorators import method_decorator

from bs4 import BeautifulSoup
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from tbx.core.blocks import StoryBlock
from tbx.core.models import RelatedLink, Tag
from tbx.core.utils.cache import get_default_cache_control_decorator


class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey("blog.BlogIndexPage", related_name="related_links")


@method_decorator(get_default_cache_control_decorator(), name="serve")
class BlogIndexPage(Page):
    template = 'patterns/pages/blog/blog_listing.html'

    intro = models.TextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
    ]

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular (exclude 'planet-drupal' as this is effectively
        # the same as Drupal and only needed for the rss feed)
        popular_tags = (
            BlogPageTagSelect.objects.all()
            .exclude(tag__name="planet-drupal")
            .values("tag")
            .annotate(item_count=models.Count("tag"))
            .order_by("-item_count")
        )

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [Tag.objects.get(id=tag["tag"]) for tag in popular_tags[:10]]

    @property
    def blog_posts(self):
        # Get list of blog pages that are descendants of this page
        blog_posts = BlogPage.objects.live().in_menu().descendant_of(self)

        # Order by most recent date first
        blog_posts = blog_posts.order_by("-date", "pk")

        return blog_posts

    def serve(self, request):
        # Get blog_posts
        blog_posts = self.blog_posts

        # Filter by tag
        tag = request.GET.get("tag")
        if tag:
            blog_posts = blog_posts.filter(tags__tag__slug=tag)

        # Pagination
        per_page = 12
        page = request.GET.get("page")
        paginator = Paginator(blog_posts, per_page)  # Show 10 blog_posts per page
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(
                request,
                "blog/includes/blog_listing.html",
                {"self": self, "blog_posts": blog_posts, "per_page": per_page},
            )
        else:
            return render(
                request,
                self.template,
                {"self": self, "blog_posts": blog_posts, "per_page": per_page},
            )

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("intro", classname="full"),
        InlinePanel("related_links", label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


# Blog page
class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey("blog.BlogPage", related_name="related_links")


# Currently hidden. These were used in the past and may be used again in the future
class BlogPageTagSelect(Orderable):
    page = ParentalKey("blog.BlogPage", related_name="tags")
    tag = models.ForeignKey(
        "torchbox.Tag", on_delete=models.CASCADE, related_name="blog_page_tag_select"
    )


class BlogPageAuthor(Orderable):
    page = ParentalKey("blog.BlogPage", related_name="authors")
    author = models.ForeignKey(
        "people.Author", on_delete=models.CASCADE, related_name="+",
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogPage(Page):
    template = "patterns/pages/blog/blog_detail.html"

    date = models.DateField("Post date")
    body = StreamField(StoryBlock())
    body_word_count = models.PositiveIntegerField(null=True, editable=False)

    feed_image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    listing_summary = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True, max_length=255)
    related_services = ParentalManyToManyField(
        "taxonomy.Service", related_name="blog_posts"
    )

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    def set_body_word_count(self):
        body_basic_html = self.body.stream_block.render_basic(self.body)
        body_text = BeautifulSoup(body_basic_html, "html.parser").get_text()
        remove_chars = string.punctuation + "“”’"
        body_words = body_text.translate(
            body_text.maketrans(dict.fromkeys(remove_chars))
        ).split()
        self.body_word_count = len(body_words)

    @property
    def related_blogs(self):
        services = self.related_services.all()
        return (
            BlogPage.objects.filter(related_services__in=services)
            .live()
            .distinct()
            .order_by("-first_published_at")
            .exclude(pk=self.pk)[:2]
        )

    @property
    def blog_index(self):
        ancestor = BlogIndexPage.objects.ancestor_of(self).order_by("-depth").first()

        if ancestor:
            return ancestor
        else:
            # No ancestors are blog indexes,
            # just return first blog index in database
            return BlogIndexPage.objects.first()

    @property
    def has_authors(self):
        return self.authors.exists()

    @property
    def read_time(self):
        return math.ceil(self.body_word_count / 275)

    content_panels = [
        FieldPanel("title", classname="full title"),
        InlinePanel("authors", label="Author"),
        FieldPanel("date"),
        StreamFieldPanel("body"),
        InlinePanel("related_links", label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel("feed_image"),
        FieldPanel("listing_summary"),
        FieldPanel("canonical_url"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
    ]


@receiver(page_published, sender=BlogPage)
def update_body_word_count_on_page_publish(instance, **kwargs):
    instance.set_body_word_count()
    instance.save(update_fields=["body_word_count"])
