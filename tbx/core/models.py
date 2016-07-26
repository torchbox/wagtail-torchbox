from __future__ import unicode_literals

from datetime import date

from django import forms
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.wagtailadmin.blocks import (CharBlock, ChooserBlock, FieldBlock,
                                         ListBlock, PageChooserBlock,
                                         RawHTMLBlock, RichTextBlock,
                                         StreamBlock, StructBlock)
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel,
                                                StreamFieldPanel)
from wagtail.wagtailadmin.utils import send_mail
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import (AbstractImage, AbstractRendition,
                                          Image)
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from tbx.core.utils import export_event


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


class WideImage(StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"

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
    wide_image = WideImage(label="Wide image")
    bustout = BustoutBlock()
    pullquote = PullQuoteBlock()
    raw_html = RawHTMLBlock(label='Raw HTML', icon="code")
    embed = EmbedBlock(icon="code")
    # photogrid = PhotoGridBlock()
    # testimonial = PullQuoteImageBlock(label="Testimonial", icon="group")
    # stats = StatsBlock()


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

    admin_form_fields = Image.admin_form_fields + (
        'credit',
    )

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
    hero_intro = models.TextField(blank=True)
    hero_video_id = models.IntegerField(blank=True, null=True, help_text="Optional. The numeric ID of a Vimeo video to replace the background image.")
    hero_video_poster_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro_title = models.TextField(blank=True)
    intro_body = models.TextField(blank=True)
    work_title = models.TextField(blank=True)
    blog_title = models.TextField(blank=True)
    clients_title = models.TextField(blank=True)

    class Meta:
        verbose_name = "Homepage"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('hero_intro'),
        InlinePanel( 'hero', label="Hero"),
        FieldPanel('intro_title'),
        FieldPanel('intro_body'),
        FieldPanel('work_title'),
        FieldPanel('blog_title'),
        FieldPanel('clients_title'),
        InlinePanel( 'clients', label="Clients"),
    ]

    @property
    def blog_posts(self):
        # Get list of blog pages.
        blog_posts = BlogPage.objects.filter(
            live=True
        )

        # Order by most recent date first
        blog_posts = blog_posts.order_by('-date')

        return blog_posts

    class HomePageHero(Orderable, RelatedLink):
        page = ParentalKey('torchbox.HomePage', related_name='hero')
        colour = models.CharField(max_length=255, help_text="Hex ref colour of link and background gradient, use #23b0b0 for default blue")
        background = models.ForeignKey(
            'torchbox.TorchboxImage',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
        )
        logo = models.ForeignKey(
            'torchbox.TorchboxImage',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
        )

        panels = RelatedLink.panels + [
            ImageChooserPanel('background'),
            ImageChooserPanel('logo'),
            FieldPanel('colour'),
        ]

    class HomePageClients(Orderable, RelatedLink):
        page = ParentalKey('torchbox.HomePage', related_name='clients')
        image = models.ForeignKey(
            'torchbox.TorchboxImage',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
        )

        panels = RelatedLink.panels + [
            ImageChooserPanel('image')
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

    panels = RelatedLink.panels + [
        ImageChooserPanel('image')
    ]


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

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

    content_panels = [
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
        InlinePanel( 'content_block', label="Content block"),
        InlinePanel( 'related_links', label="Related links"),
        InlinePanel( 'clients', label="Clients"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('show_in_play_menu'),
        ImageChooserPanel('feed_image'),
    ]

# About page

class AbstractBaseService(Orderable):
    title = models.TextField()
    svg = models.TextField(null=True)
    description = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('svg')
    ]

    class Meta:
        abstract = True


class AboutPageService(AbstractBaseService):
    page = ParentalKey('torchbox.AboutPage', related_name='services')


class AboutPageOffice(Orderable):
    page = ParentalKey('torchbox.AboutPage', related_name='offices')
    title = models.TextField()
    svg = models.TextField(null=True)
    description = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('svg')
    ]

class AboutPageValues(Orderable):
    page = ParentalKey('torchbox.AboutPage', related_name='values')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]

class AboutPageInvolvement(Orderable):
    page = ParentalKey('torchbox.AboutPage', related_name='involvement')
    title = models.TextField()
    svg = models.TextField(null=True)
    description = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('svg')
    ]

class AboutPageClients(Orderable, RelatedLink):
    page = ParentalKey('torchbox.AboutPage', related_name='clients')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = RelatedLink.panels + [
        ImageChooserPanel('image')
    ]

class AboutPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    values_title = models.TextField(blank=True)
    involvement_title = models.TextField(blank=True)

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        FieldPanel('heading'),
        FieldPanel('intro', classname='full'),
        InlinePanel('services', label='Services'),
        InlinePanel('offices', label='Offices'),
        FieldPanel('values_title'),
        InlinePanel('values', label='Values'),
        FieldPanel('involvement_title'),
        InlinePanel('involvement', label='Involvement'),
        InlinePanel('clients', label='Clients')
    ]


# Services page

class ServicesPageService(AbstractBaseService):
    page = ParentalKey('torchbox.ServicesPage', related_name='services')


class ServicesPage(Page):
    main_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading = models.TextField(blank=True)
    intro = models.TextField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        FieldPanel('heading'),
        FieldPanel('intro', classname='full'),
        InlinePanel('services', label='Services'),
    ]


# Blog index page

class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('torchbox.BlogIndexPage', related_name='related_links')


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

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
        # and are not marketing_only
        blog_posts = BlogPage.objects.filter(
            live=True,
            path__startswith=self.path
        ).exclude(marketing_only=True)

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
    page = ParentalKey('torchbox.BlogPage', related_name='related_links')


class BlogPageTagList(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

register_snippet(BlogPageTagList)


class BlogPageTagSelect(Orderable):
    page = ParentalKey('torchbox.BlogPage', related_name='tags')
    tag = models.ForeignKey(
        'torchbox.BlogPageTagList',
        related_name='blog_page_tag_select'
    )


class BlogPageAuthor(Orderable):
    page = ParentalKey('torchbox.BlogPage', related_name='related_author')
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
    homepage_color = models.TextField("Homepage colour (orange, blue, white) if left blank will display image", blank=True)
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

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )
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
        FieldPanel('homepage_color'),
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
        FieldPanel('marketing_only'),
    ]


# Jobs index page
class ReasonToJoin(Orderable):
    page = ParentalKey('torchbox.JobIndexPage', related_name='reasons_to_join')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=511)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('body')
    ]


class JobIndexPageJob(Orderable):
    page = ParentalKey('torchbox.JobIndexPage', related_name='job')
    job_title = models.CharField(max_length=255)
    job_intro = models.CharField(max_length=255)
    url = models.URLField(null=True)
    location = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('job_title'),
        FieldPanel('job_intro'),
        FieldPanel("url"),
        FieldPanel("location"),
    ]


class JobIndexPage(Page):
    intro = RichTextField(blank=True)
    no_jobs_that_fit = models.URLField(null=True)
    terms_and_conditions = models.URLField(null=True)
    refer_a_friend = models.URLField(null=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    def get_context(self, request, *args, **kwargs):
        context = super(
            JobIndexPage, self
        ).get_context(request, *args, **kwargs)
        context['jobs'] = self.job.all()
        context['blogs'] = BlogPage.objects.live().order_by('-date')[:4]
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        FieldPanel('no_jobs_that_fit', classname="full"),
        FieldPanel('terms_and_conditions', classname="full"),
        FieldPanel('refer_a_friend', classname="full"),
        InlinePanel('job', label="Job"),
        InlinePanel('reasons_to_join', label="Reasons To Join"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


# Work page
class WorkPageTagSelect(Orderable):
    page = ParentalKey('torchbox.WorkPage', related_name='tags')
    tag = models.ForeignKey(
        'torchbox.BlogPageTagList',
        related_name='work_page_tag_select'
    )


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


class WorkPageAuthor(Orderable):
    page = ParentalKey('torchbox.WorkPage', related_name='related_author')
    author = models.ForeignKey(
        'torchbox.PersonPage',
        null=True,
        blank=True,
        related_name='+'
    )

    panels = [
        PageChooserPanel('author'),
    ]


class WorkPage(Page):
    author_left = models.CharField(max_length=255, blank=True, help_text='author who has left Torchbox')
    summary = models.CharField(max_length=255)
    descriptive_title = models.CharField(max_length=255)
    intro = RichTextField("Intro (deprecated. Use streamfield instead)", blank=True)
    body = RichTextField("Body (deprecated. Use streamfield instead)", blank=True)
    homepage_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    marketing_only = models.BooleanField(default=False, help_text='Display this work item only on marketing landing page')
    streamfield = StreamField(StoryBlock())

    show_in_play_menu = models.BooleanField(default=False)

    @property
    def work_index(self):
        # Find work index in ancestors
        for ancestor in reversed(self.get_ancestors()):
            if isinstance(ancestor.specific, WorkIndexPage):
                return ancestor

        # No ancestors are work indexes,
        # just return first work index in database
        return WorkIndexPage.objects.first()

    @property
    def has_authors(self):
        for author in self.related_author.all():
            if author.author:
                return True

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('descriptive_title'),
        InlinePanel('related_author', label="Author"),
        FieldPanel('author_left'),
        FieldPanel('summary'),
        FieldPanel('intro', classname="full"),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('streamfield'),
        ImageChooserPanel('homepage_image'),
        InlinePanel('screenshots', label="Screenshots"),
        InlinePanel('tags', label="Tags"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('show_in_play_menu'),
        FieldPanel('marketing_only'),
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
        # and are not marketing only
        works = WorkPage.objects.filter(
            live=True,
            path__startswith=self.path
        ).exclude(marketing_only=True)

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

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        FieldPanel('hide_popular_tags'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
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


    search_fields = Page.search_fields + (
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('biography'),
    )

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('role'),
        FieldPanel('intro', classname="full"),
        FieldPanel('biography', classname="full"),
        ImageChooserPanel('image'),
        MultiFieldPanel(ContactFields.panels, "Contact"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]


# Person index
class PersonIndexPage(Page):
    intro = RichTextField(blank=True)
    show_in_play_menu = models.BooleanField(default=False)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

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

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
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


class GoogleAdGrantApplication(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        ordering = ['-date']


class GoogleAdGrantApplicationForm(forms.ModelForm):
    class Meta:
        model = GoogleAdGrantApplication
        fields = [
            'name', 'email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Your charity's name"}),
            'email': forms.TextInput(attrs={'placeholder': "Your email address"})
        }


class GoogleAdGrantsPageGrantsManaged(models.Model):
    page = ParentalKey('torchbox.GoogleAdGrantsPage', related_name="grants_managed")
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]


class GoogleAdGrantsPageQuote(Orderable):
    page = ParentalKey('torchbox.GoogleAdGrantsPage', related_name="quotes")
    text = models.TextField()
    person_name = models.CharField(max_length=255)
    organisation_name = models.CharField(max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('person_name'),
        FieldPanel('organisation_name'),
    ]


class GoogleAdGrantsAccreditations(Orderable):
    page = ParentalKey('torchbox.GoogleAdGrantsPage', related_name="accreditations")
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]


class GoogleAdGrantsPage(Page):
    intro = RichTextField()
    form_title = models.CharField(max_length=255)
    form_subtitle = models.CharField(max_length=255)
    form_button_text = models.CharField(max_length=255)
    to_address = models.EmailField(
        verbose_name='to address', blank=True,
        help_text="Optional - form submissions will be emailed to this address"
    )
    body = RichTextField()
    grants_managed_title = models.CharField(max_length=255)
    call_to_action_title = models.CharField(max_length=255, blank=True)
    call_to_action_embed_url = models.URLField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body')
    )

    def get_context(self, request):
        form = GoogleAdGrantApplicationForm()
        context = super(GoogleAdGrantsPage, self).get_context(request)
        context['form'] = form
        return context

    def serve(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            form = GoogleAdGrantApplicationForm(request.POST)
            if form.is_valid():
                form.save()

                if self.to_address:
                    subject = "{} form submission".format(self.title)
                    content = '\n'.join([x[1].label + ': ' + str(form.data.get(x[0])) for x in form.fields.items()])
                    send_mail(subject, content, [self.to_address],)
                return render(
                    request,
                    'torchbox/includes/ad_grant_application_landing.html',
                    {'self': self, 'form': form}
                )
            else:
                return render(
                    request,
                    'torchbox/includes/ad_grant_application_form.html',
                    {'self': self, 'form': form}
                )
        else:
            return super(GoogleAdGrantsPage, self).serve(request)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
        MultiFieldPanel([
            FieldPanel('form_title'),
            FieldPanel('form_subtitle'),
            FieldPanel('form_button_text'),
            FieldPanel('to_address'),
        ], "Application Form"),
        MultiFieldPanel([
            FieldPanel('grants_managed_title'),
            InlinePanel('grants_managed', label="Grants Managed")
        ], "Grants Managed Section"),
        InlinePanel('quotes', label="Quotes"),
        MultiFieldPanel([
            FieldPanel('call_to_action_title'),
            FieldPanel('call_to_action_embed_url'),
            InlinePanel('accreditations', label="Accreditations")
        ], "Call To Action")
    ]


# Sign-up for something page
class SignUpFormPageBullet(Orderable):
    page = ParentalKey('torchbox.SignUpFormPage', related_name='bullet_points')
    icon = models.CharField(max_length=100, choices=(
        ('torchbox/includes/svg/bulb-svg.html','Light bulb'),
        ('torchbox/includes/svg/pro-svg.html','Chart'),
        ('torchbox/includes/svg/tick-svg.html','Tick'),
    ))
    title = models.CharField(max_length=100)
    body = models.TextField()

    panels = [
        FieldPanel('icon'),
        FieldPanel('title'),
        FieldPanel('body'),
    ]


class SignUpFormPageLogo(Orderable):
    page = ParentalKey('torchbox.SignUpFormPage', related_name='logos')
    logo = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('logo'),
    ]


class SignUpFormPageQuote(Orderable):
    page = ParentalKey('torchbox.SignUpFormPage', related_name='quotes')
    quote = models.TextField()
    author = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)

    panels = [
        FieldPanel('quote'),
        FieldPanel('author'),
        FieldPanel('organisation'),
    ]


class SignUpFormPageResponse(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.email


class SignUpFormPageForm(forms.ModelForm):
    class Meta:
        model = SignUpFormPageResponse
        fields = [
            'email',
        ]
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': "Enter your email address"}),
        }


class SignUpFormPage(Page):
    formatted_title = models.CharField(
        max_length=255, blank=True,
        help_text="This is the title displayed on the page, not the document "
        "title tag. HTML is permitted. Be careful."
    )
    intro = RichTextField()
    call_to_action_text = models.CharField(
        max_length=255, help_text="Displayed above the email submission form."
    )
    call_to_action_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    form_button_text = models.CharField(max_length=255)
    thank_you_text = models.CharField(max_length=255,
                                      help_text="Displayed on successful form submission.")
    email_subject = models.CharField(max_length=100, verbose_name='subject')
    email_body = models.TextField(verbose_name='body')
    email_attachment = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name='attachment',
    )
    email_from_address = models.EmailField(
        verbose_name='from address',
        help_text="Anything ending in @torchbox.com is good.")

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('formatted_title'),
        ], 'Title'),
        FieldPanel('intro', classname="full"),
        InlinePanel('bullet_points', label="Bullet points"),
        InlinePanel('logos', label="Logos"),
        InlinePanel('quotes', label="Quotes"),
        MultiFieldPanel([
            FieldPanel('call_to_action_text'),
            ImageChooserPanel('call_to_action_image'),
            FieldPanel('form_button_text'),
            FieldPanel('thank_you_text'),
        ], 'Form'),
        MultiFieldPanel([
            FieldPanel('email_subject'),
            FieldPanel('email_body'),
            DocumentChooserPanel('email_attachment'),
            FieldPanel('email_from_address'),
        ], 'Email'),
    ]

    def get_context(self, request):
        form = SignUpFormPageForm()
        context = super(SignUpFormPage, self).get_context(request)
        context['form'] = form
        return context

    def serve(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            form = SignUpFormPageForm(request.POST)

            if form.is_valid():
                form.save()
                self.send_email_response(form.cleaned_data['email'])
                return render(
                    request,
                    'torchbox/includes/sign_up_form_page_landing.html',
                    {'page': self, 'form': form}
                )
            else:
                return render(
                    request,
                    'torchbox/includes/sign_up_form_page_form.html',
                    {'page': self, 'form': form}
                )
        else:
            return super(SignUpFormPage, self).serve(request)

    def send_email_response(self, to_address):
        email_message = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.email_from_address,
            to=[to_address],
        )
        email_message.attach_file(self.email_attachment.file.path)
        email_message.send()


class AbstractBaseMarketingLandingPageRelatedLink(Orderable, RelatedLink):
    email_link = models.EmailField("Email link", blank=True,
                                   help_text="Enter email address only, without 'mailto:'")

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        elif self.link_external:
            return self.link_external
        else:
            return "mailto:{}".format(self.email_link)

    panels = RelatedLink.panels + [
        FieldPanel('email_link')
    ]

    class Meta:
        abstract = True


class MarketingLandingPageHeaderRelatedLink(AbstractBaseMarketingLandingPageRelatedLink):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='header_related_links')


class MarketingLandingPageIntroRelatedLink(AbstractBaseMarketingLandingPageRelatedLink):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='intro_related_links')


class MarketingLandingPagePageClients(Orderable, RelatedLink):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='clients')
    image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = RelatedLink.panels + [
        ImageChooserPanel('image')
    ]


class MarketingLandingPageFeaturedItem(Orderable):
    page = ParentalKey('torchbox.MarketingLandingPage', related_name='featured_items')
    related_page = models.ForeignKey('wagtailcore.Page', related_name='+')

    panels = [
        PageChooserPanel('related_page', ['torchbox.BlogPage', 'torchbox.WorkPage'])
    ]


class MarketingLandingPage(Page):
    intro = models.TextField('header text', blank=True)
    hero_video_id = models.IntegerField(blank=True, null=True, help_text="Optional. The numeric ID of a Vimeo video to replace the background image.")
    hero_video_poster_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro_subtitle = models.CharField('intro subtitle', max_length=255, blank=True)

    class Meta:
        verbose_name = "Marketing Landing Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro'),
        FieldPanel('hero_video_id'),
        ImageChooserPanel('hero_video_poster_image'),
        InlinePanel('header_related_links', label="Header related items"),
        FieldPanel('intro_subtitle'),
        InlinePanel('intro_related_links', label="Intro related items"),
        InlinePanel('featured_items', label="Featured Items"),
        InlinePanel( 'clients', label="Clients"),
    ]

# Contact page

class ContactFormField(AbstractFormField):
    page = ParentalKey('Contact', related_name='form_fields')


class Contact(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    class Meta:
        verbose_name = "Contact Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email")
    ]

from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class GlobalSettings(BaseSetting):
    class Meta:
        verbose_name = 'Global Settings'
    ContactTelephone = models.CharField(max_length=255, help_text='Telephone')
    ContactEmail = models.CharField(max_length=255, help_text='Email address')
    ContactTwitter = models.CharField(max_length=255, help_text='Twitter')
    EmailNewsletterTeaser = models.CharField(max_length=255, help_text='Text that sits above the email newsletter')
    OxfordAddressTitle = models.CharField(max_length=255, help_text='Full address')
    OxfordAddress = models.CharField(max_length=255, help_text='Full address')
    OxfordAddressLink = models.URLField(max_length=255, help_text='Link to google maps')
    OxfordAddressSVG = models.CharField(max_length=9000, help_text='Paste SVG code here')
    BristolAddressTitle = models.CharField(max_length=255, help_text='Full address')
    BristolAddress = models.CharField(max_length=255, help_text='Full address')
    BristolAddressLink = models.URLField(max_length=255, help_text='Link to google maps')
    BristolAddressSVG = models.CharField(max_length=9000, help_text='Paste SVG code here')
    PhiliAddressTitle = models.CharField(max_length=255, help_text='Full address')
    PhiliAddress = models.CharField(max_length=255, help_text='Full address')
    PhiliAddressLink = models.URLField(max_length=255, help_text='Link to google maps')
    PhiliAddressSVG = models.CharField(max_length=9000, help_text='Paste SVG code here')
