from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property

from taggit.models import ItemBase, TagBase

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from tbx.core.blocks import StoryBlock
from tbx.core.utils.cache import get_default_cache_control_decorator
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@method_decorator(get_default_cache_control_decorator(), name="serve")
class TechBlogIndexPage(Page):
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
    body = StreamField(StoryBlock(), use_json_field=True)
    tags = ClusterTaggableManager(through=TaggedTechBlogPost, blank=True)

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
