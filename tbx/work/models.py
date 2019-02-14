from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import render
from django.utils.decorators import method_decorator

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, StreamFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from tbx.core.blocks import StoryBlock
from tbx.core.models import Tag, purge_homepage, purge_parent_index
from tbx.core.utils.cache import get_default_cache_control_decorator


class WorkPageTagSelect(Orderable):
    page = ParentalKey('work.WorkPage', related_name='tags')
    tag = models.ForeignKey(
        'torchbox.Tag',
        on_delete=models.CASCADE,
        related_name='work_page_tag_select'
    )


class WorkPageScreenshot(Orderable):
    page = ParentalKey('work.WorkPage', related_name='screenshots')
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
    page = ParentalKey('work.WorkPage', related_name='authors')
    author = models.ForeignKey(
        'people.Author',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        SnippetChooserPanel('author'),
    ]


class WorkPage(Page):
    summary = models.CharField(max_length=255)
    descriptive_title = models.CharField(max_length=255)
    homepage_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'torchbox.TorchboxImage',
        help_text='Image used on listings and social media.',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(StoryBlock())
    visit_the_site = models.URLField(blank=True)

    @property
    def work_index(self):
        ancestor = WorkIndexPage.objects.ancestor_of(self).order_by('-depth').first()

        if ancestor:
            return ancestor
        else:
            # No ancestors are work indexes,
            # just return first work index in database
            return WorkIndexPage.objects.first()

    @property
    def has_authors(self):
        return self.authors.exists()

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('descriptive_title'),
        InlinePanel('authors', label="Author"),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
        ImageChooserPanel('homepage_image'),
        InlinePanel('screenshots', label="Screenshots"),
        InlinePanel('tags', label="Tags"),
        FieldPanel('visit_the_site'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]


# Work index page
@method_decorator(get_default_cache_control_decorator(), name='serve')
class WorkIndexPage(Page):
    intro = RichTextField(blank=True)

    hide_popular_tags = models.BooleanField(default=False)

    def get_popular_tags(self):
        # Get a ValuesQuerySet of tags ordered by most popular
        popular_tags = WorkPageTagSelect.objects.all().values('tag').annotate(item_count=models.Count('tag')).order_by('-item_count')

        # Return first 10 popular tags as tag objects
        # Getting them individually to preserve the order
        return [Tag.objects.get(id=tag['tag']) for tag in popular_tags[:10]]

    @property
    def works(self):
        # Get list of work pages that are descendants of this page
        return WorkPage.objects.descendant_of(self).live()

    def serve(self, request):
        # Get work pages
        works = self.works

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            works = works.filter(tags__tag__slug=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(works, 12)  # Show 10 works per page
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
    ]


@receiver(page_published, sender=WorkPage)
def work_page_published_handler(instance, **kwargs):
    purge_parent_index(WorkIndexPage, instance)
    purge_homepage()


@receiver(pre_delete, sender=WorkPage)
def work_page_deleted_handler(instance, **kwargs):
    purge_parent_index(WorkIndexPage, instance)
    purge_homepage()
