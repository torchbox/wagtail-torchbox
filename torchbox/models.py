from __future__ import unicode_literals

from datetime import date
from django import forms

from django.db import models
from django.db.models.signals import pre_delete
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailadmin.blocks import ChooserBlock, StructBlock, ListBlock, \
    StreamBlock, FieldBlock, CharBlock, RichTextBlock, PageChooserBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.models import AbstractImage, AbstractRendition
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase

from torchbox.utils import export_event

### Streamfield blocks and config ###

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left','Wrap left'),
        ('right','Wrap right'),
        ('half','Half width'),
        ('full','Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alignment = ImageFormatChoiceBlock()
    caption = CharBlock()
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"


class PhotoGridBlock(StructBlock):
    images = ListBlock(ImageChooserBlock())

    class Meta:
        icon = "grip"


class PullQuoteBlock(StructBlock):
    quote = CharBlock(classname="quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class PullQuoteImageBlock(StructBlock):
    quote = CharBlock()
    attribution = CharBlock()
    image = ImageChooserBlock(required=False)


class BustoutBlock(StructBlock):
    image = ImageChooserBlock()
    text = RichTextBlock()

    class Meta:
        icon = "pick"


class StatsBlock(StructBlock):
    pass

    class Meta:
        icon = "order"


class StoryBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image")
    bustout = BustoutBlock()
    pullquote = PullQuoteBlock()
    raw_html = RawHTMLBlock(label='Raw HTML', icon="code")
    # photogrid = PhotoGridBlock()
    # testimonial = PullQuoteImageBlock(label="Testimonial", icon="group")
    # stats = StatsBlock()



COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
)


# A couple of abstract classes that contain commonly used fields
class ContentBlock(models.Model):
    content = RichTextField()

    panels = [
        FieldPanel('content'),
    ]

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


# Carousel items
class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Advert Snippet
class AdvertPlacement(models.Model):
    page = ParentalKey('wagtailcore.Page', related_name='advert_placements')
    advert = models.ForeignKey('torchbox.Advert', related_name='+')


class Advert(models.Model):
    page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='adverts',
        null=True,
        blank=True
    )
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __unicode__(self):
        return self.text

register_snippet(Advert)


# Custom image
class TorchboxImage(AbstractImage):
    credit = models.CharField(max_length=255, blank=True)

    @property
    def credit_text(self):
        return self.credit


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=TorchboxImage)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


class TorchboxRendition(AbstractRendition):
    image = models.ForeignKey('TorchboxImage', related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=TorchboxRendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


class HomePage(Page):
    intro = models.TextField(blank=True)
    hero_video_id = models.IntegerField(blank=True, null=True, help_text="Optional. The numeric ID of a Vimeo video to replace the background image.")
    hero_video_poster_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_name = "Homepage"

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro'),
    FieldPanel('hero_video_id'),
    ImageChooserPanel('hero_video_poster_image'),
]

HomePage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
]


# Standard page

class StandardPageContentBlock(Orderable, ContentBlock):
    page = ParentalKey('torchbox.StandardPage', related_name='content_block')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.StandardPage', related_name='related_links')


class StandardPageClients(Orderable, RelatedLink):
    page = ParentalKey('torchbox.StandardPage', related_name='clients')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

StandardPageClients.panels = StandardPageClients.panels + [
    ImageChooserPanel('image')]


class StandardPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    credit = models.CharField(max_length=255, blank=True)
    heading = RichTextField(blank=True)
    quote = models.CharField(max_length=255, blank=True)
    intro = RichTextField("Intro (deprecated. Use streamfield instead)", blank=True)
    middle_break = RichTextField(blank=True)
    body = RichTextField("Body (deprecated. Use streamfield instead)", blank=True)
    streamfield = StreamField(StoryBlock())
    email = models.EmailField(blank=True)

    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    show_in_play_menu = models.BooleanField(default=False)

    indexed_fields = ('intro', 'body', )
    search_name = None

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('main_image'),
    FieldPanel('credit', classname="full"),
    FieldPanel('heading', classname="full"),
    FieldPanel('quote', classname="full"),
    FieldPanel('intro', classname="full"),
    FieldPanel('middle_break', classname="full"),
    FieldPanel('body', classname="full"),
    StreamFieldPanel('streamfield'),
    FieldPanel('email', classname="full"),
    InlinePanel(StandardPage, 'content_block', label="Content block"),
    InlinePanel(StandardPage, 'related_links', label="Related links"),
    InlinePanel(StandardPage, 'clients', label="Clients"),
]

StandardPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    FieldPanel('show_in_play_menu'),
    ImageChooserPanel('feed_image'),
]


# Services page

class ServicesPageContentBlock(Orderable, ContentBlock):
    page = ParentalKey('torchbox.ServicesPage', related_name='content_block')


class ServicesPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.ServicesPage', related_name='related_links')


class ServicesPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('intro', 'body', )
    search_name = None

ServicesPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('body', classname="full"),
    InlinePanel(ServicesPage, 'content_block', label="Content block"),
    InlinePanel(ServicesPage, 'related_links', label="Related links"),
]

ServicesPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


# Blog index page

class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.BlogIndexPage', related_name='related_links')


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    indexed_fields = ('intro', )
    search_name = "Blog"

    show_in_play_menu = models.BooleanField(default=False)

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular
        popular_tags = BlogPageTagSelect.objects.all().values('tag').annotate(item_count=models.Count('tag')).order_by('-item_count')

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [BlogPageTagList.objects.get(id=tag['tag']) for tag in popular_tags[:10]]

    @property
    def blog_posts(self):
        # Get list of blog pages that are descendants of this page
        blog_posts = BlogPage.objects.filter(
            live=True,
            path__startswith=self.path
        )

        # Order by most recent date first
        blog_posts = blog_posts.order_by('-date')

        return blog_posts

    def serve(self, request):
        # Get blog_posts
        blog_posts = self.blog_posts

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blog_posts = blog_posts.filter(tags__tag__slug=tag)

        # Pagination
        per_page = 10
        page = request.GET.get('page')
        paginator = Paginator(blog_posts, per_page)  # Show 10 blog_posts per page
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, "torchbox/includes/blog_listing.html", {
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


BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(BlogIndexPage, 'related_links', label="Related links"),
]

BlogIndexPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    FieldPanel('show_in_play_menu'),
]


# Blog page
class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.BlogPage', related_name='related_links')


class BlogPageTagList(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class BlogPageTagSelect(Orderable):
    page = ParentalKey('torchbox.BlogPage', related_name='tags')
    tag = models.ForeignKey(
        'torchbox.BlogPageTagList',
        related_name='blog_page_tag_select'
    )

BlogPageTagSelect.content_panels = [
    FieldPanel('tag'),
]


class BlogPageAuthor(Orderable):
    page = ParentalKey('torchbox.BlogPage', related_name='related_author')
    author = models.ForeignKey(
        'torchbox.PersonPage',
        null=True,
        blank=True,
        related_name='+'
    )

    panels = [
        PageChooserPanel('author', 'torchbox.PersonPage')
    ]


class BlogPage(Page):
    intro = RichTextField("Intro (used only for blog index listing)", blank=True)
    body = RichTextField("body (deprecated. Use streamfield instead)", blank=True)
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

    indexed_fields = ('body', )
    search_name = "Blog Entry"

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

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    InlinePanel(BlogPage, 'related_author', label="Author"),
    FieldPanel('author_left'),
    FieldPanel('date'),
    FieldPanel('intro', classname="full"),
    FieldPanel('body', classname="full"),
    StreamFieldPanel('streamfield'),
    InlinePanel(BlogPage, 'related_links', label="Related links"),
    InlinePanel(BlogPage, 'tags', label="Tags")
]

BlogPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


# Jobs index page
class JobIndexPageContentBlock(Orderable, ContentBlock):
    page = ParentalKey('torchbox.JobIndexPage', related_name='content_block')


class JobIndexPageJob(Orderable):
    page = ParentalKey('torchbox.JobIndexPage', related_name='job')
    job_title = models.CharField(max_length=255)
    url = models.URLField(null=True)
    location = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('job_title'),
        FieldPanel("url"),
        FieldPanel("location"),
    ]


class JobIndexPage(Page):
    intro = RichTextField(blank=True)

    indexed_fields = ('intro', 'body', )

    @property
    def jobs(self):
        jobs = self.job.all()

        return jobs

    def serve(self, request):
        # Get jobs
        jobs = self.jobs

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(jobs, 10)  # Show 10 jobs per page
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        return render(request, self.template, {
            'self': self,
            'jobs': jobs,
        })


JobIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(JobIndexPage, 'content_block', label="Content block"),
    InlinePanel(JobIndexPage, 'job', label="Job"),
]

JobIndexPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
]


# Work page
class WorkPageTagSelect(Orderable):
    page = ParentalKey('torchbox.WorkPage', related_name='tags')
    tag = models.ForeignKey(
        'torchbox.BlogPageTagList',
        related_name='work_page_tag_select'
    )

WorkPageTagSelect.content_panels = [
    FieldPanel('tag'),
]


class WorkPageScreenshot(Orderable):
    page = ParentalKey('torchbox.WorkPage', related_name='screenshots')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class WorkPage(Page):
    summary = models.CharField(max_length=255)
    intro = RichTextField("Intro (deprecated. Use streamfield instead)", blank=True)
    body = RichTextField("Body (deprecated. Use streamfield instead)", blank=True)
    homepage_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    streamfield = StreamField(StoryBlock())

    @property
    def work_index(self):
        # Find work index in ancestors
        for ancestor in reversed(self.get_ancestors()):
            if isinstance(ancestor.specific, WorkIndexPage):
                return ancestor

        # No ancestors are work indexes,
        # just return first work index in database
        return WorkIndexPage.objects.first()

WorkPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('summary'),
    FieldPanel('intro', classname="full"),
    FieldPanel('body', classname="full"),
    StreamFieldPanel('streamfield'),
    ImageChooserPanel('homepage_image'),
    InlinePanel(WorkPage, 'screenshots', label="Screenshots"),
    InlinePanel(BlogPage, 'tags', label="Tags"),
]


# Work index page
class WorkIndexPage(Page):
    intro = RichTextField(blank=True)

    show_in_play_menu = models.BooleanField(default=False)
    hide_popular_tags = models.BooleanField(default=False)

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular
        popular_tags = WorkPageTagSelect.objects.all().values('tag').annotate(item_count=models.Count('tag')).order_by('-item_count')

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [BlogPageTagList.objects.get(id=tag['tag']) for tag in popular_tags[:10]]

    @property
    def works(self):
        # Get list of work pages that are descendants of this page
        works = WorkPage.objects.filter(
            live=True,
            path__startswith=self.path
        )

        return works

    def serve(self, request):
        # Get work pages
        works = self.works

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            works = works.filter(tags__tag__slug=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(works, 10)  # Show 10 works per page
        try:
            works = paginator.page(page)
        except PageNotAnInteger:
            works = paginator.page(1)
        except EmptyPage:
            works = paginator.page(paginator.num_pages)

        return render(request, self.template, {
            'self': self,
            'works': works,
        })


WorkIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('hide_popular_tags'),
]

WorkIndexPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    FieldPanel('show_in_play_menu'),
]


# Person page
class PersonPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.PersonPage', related_name='related_links')


class PersonPage(Page, ContactFields):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('first_name', 'last_name', 'intro', 'biography')
    search_name = "Person"

PersonPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('role'),
    FieldPanel('intro', classname="full"),
    FieldPanel('biography', classname="full"),
    ImageChooserPanel('image'),
    MultiFieldPanel(ContactFields.panels, "Contact"),
    InlinePanel(PersonPage, 'related_links', label="Related links"),
]

PersonPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


# Person index
class PersonIndexPage(Page):
    intro = RichTextField(blank=True)
    show_in_play_menu = models.BooleanField(default=False)
    indexed_fields = ('intro', )

    @property
    def people(self):
        # Get list of person pages that are descendants of this page
        people = PersonPage.objects.filter(
            live=True,
            path__startswith=self.path
        )

        return people

    def serve(self, request):
        # Get people
        people = self.people

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(people, 10)  # Show 10 jobs per page
        try:
            people = paginator.page(page)
        except PageNotAnInteger:
            people = paginator.page(1)
        except EmptyPage:
            people = paginator.page(paginator.num_pages)

        return render(request, self.template, {
            'self': self,
            'people': people,
        })


PersonIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
]

PersonIndexPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    FieldPanel('show_in_play_menu'),
]


class TshirtPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

TshirtPage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('main_image'),
]
