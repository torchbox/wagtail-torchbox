from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property

from taggit.models import ItemBase, TagBase

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from tbx.core.utils.cache import get_default_cache_control_decorator
from tbx.core.utils.text import get_read_time, get_word_count
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.signals import page_published
from wagtail.snippets.models import register_snippet

from .blocks import TechBlogBlock
from .feeds import TechBlogFeed


@method_decorator(get_default_cache_control_decorator(), name="serve")
class TechBlogIndexPage(RoutablePageMixin, Page):
    max_count = 1
    template = "patterns/pages/tech_blog/tech_blog_listing.html"

    subpage_types = ["TechBlogPage"]

    @property
    def blog_posts(self):
        # Get list of blog pages that are descendants of this page
        blog_posts = TechBlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blog_posts = blog_posts.order_by("-date", "pk")

        return blog_posts

    def get_context(self, request):
        blog_posts = self.blog_posts

        # Filter by related_service slug
        slug_filter = request.GET.get("filter")
        if slug_filter:
            blog_posts = blog_posts.filter(tags__slug=slug_filter)

        paginator = Paginator(blog_posts, per_page=10)

        page_num = request.GET.get("page")

        try:
            page = paginator.get_page(page_num)
        except PageNotAnInteger:
            page = paginator.get_page(1)
        except EmptyPage:
            page = None

        context = super().get_context(request)
        context["blog_posts"] = page
        context["tags"] = TechBlogTag.objects.all()
        return context

    @route(r"^feed/$")
    def feed(self, request):
        return TechBlogFeed(
            self.blog_posts,
            self.get_full_url(request),
            self.title,
        )(request)


class TechBlogPageAuthor(Orderable):
    page = ParentalKey("tech_blog.TechBlogPage", related_name="authors")
    author = models.ForeignKey(
        "people.Author",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("author"),
    ]


@register_snippet
class TechBlogTag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "Tech Blog Tag"


class TaggedTechBlogPost(ItemBase):
    tag = models.ForeignKey(
        TechBlogTag, related_name="tagged_blog_posts", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to="tech_blog.TechBlogPage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class TechBlogPage(Page):
    template = "patterns/pages/tech_blog/tech_blog_post.html"

    parent_page_types = ["TechBlogIndexPage"]

    date = models.DateField("Post date")
    body = StreamField(TechBlogBlock(), use_json_field=True)
    tags = ClusterTaggableManager(through=TaggedTechBlogPost, blank=True)
    body_word_count = models.PositiveIntegerField(null=True, editable=False)

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    @cached_property
    def blog_index(self):
        return TechBlogIndexPage.objects.first()

    @property
    def author(self):
        """Safely return the first author if one exists."""
        author = self.authors.first()
        if author:
            return author.author
        return None

    content_panels = [
        FieldPanel("title", classname="title"),
        InlinePanel("authors", label="Author", min_num=1),
        FieldPanel("date"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [FieldPanel("tags")]

    def set_body_word_count(self):
        body_basic_html = self.body.stream_block.render_basic(self.body)
        self.body_word_count = get_word_count(body_basic_html)

    @property
    def read_time(self):
        return get_read_time(self.body_word_count)


@receiver(page_published, sender=TechBlogPage)
def update_body_word_count_on_page_publish(instance, **kwargs):
    instance.set_body_word_count()
    instance.save(update_fields=["body_word_count"])
