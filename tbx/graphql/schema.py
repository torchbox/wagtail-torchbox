import graphene
from graphene.types import Scalar
from wagtail.core.blocks import StreamValue
from wagtail.core.rich_text import RichText

from tbx.core.models import BlogPage, TorchboxImage, WorkPage

from .streamfield import StreamFieldSerialiser


class Page(graphene.Interface):
    title = graphene.String()
    slug = graphene.String()


class StreamField(Scalar):
    @staticmethod
    def serialize(val):
        return StreamFieldSerialiser().serialise_stream_block(val)


class ImageRendition(graphene.ObjectType):
    url = graphene.String()
    width = graphene.Int()
    height = graphene.Int()


class Image(graphene.ObjectType):
    FORMATS = {
        'quarter': 'width-400',  # Used by aligned image when alignment is either "left" or "right"
        'half': 'width-800',  # Used by aligned image when alignment is "half"
        'full': 'width-1280',  # Used by aligned image when alignment is "full"
        'logo': 'max-250x80',  # Used by logo block
    }

    id = graphene.Int()
    alt = graphene.String()
    rendition = graphene.Field(ImageRendition, format=graphene.String())
    width = graphene.Int()
    height = graphene.Int()

    def resolve_alt(self, info):
        return self.title

    def resolve_rendition(self, info, format):
        if format in Image.FORMATS:
            return self.get_rendition(Image.FORMATS[format])

        # TODO: Error


class BlogPost(graphene.ObjectType):
    body = StreamField()
    author_left = graphene.String()
    date = graphene.Date()
    feed_image = graphene.Field(Image)
    marketing_only = graphene.Boolean()

    def resolve_body(self, info):
        if self.streamfield:
            return self.streamfield

        if self.body:
            # Old rich text field, pretend it's a streamfield block
            return StreamValue(
                BlogPage._meta.get_field('streamfield').stream_block,
                [
                    ('paragraph', RichText(self.body)),
                ]
            )

        return None

    class Meta:
        interfaces = [Page]


class CaseStudy(graphene.ObjectType):
    class Meta:
        interfaces = [Page]


class Query(graphene.ObjectType):
    blog_posts = graphene.List(BlogPost)
    case_studies = graphene.List(CaseStudy)
    images = graphene.List(Image, ids=graphene.List(graphene.Int))

    def resolve_blog_posts(self, info, **kwargs):
        return BlogPage.objects.order_by('-date')

    def resolve_case_studies(self, info, **kwargs):
        return WorkPage.objects.live().public().order_by('-first_published_at')

    def resolve_images(self, info, **kwargs):
        images = TorchboxImage.objects.all()
        if 'ids' in kwargs:
            images = images.filter(id__in=kwargs['ids'])

        return images


schema = graphene.Schema(
    query=Query,
)
