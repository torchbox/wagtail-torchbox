import graphene
from graphene.types import Scalar

from tbx.blog.models import BlogPage
from tbx.core.models import TorchboxImage
from tbx.people.models import Author, PersonPage
from tbx.services.models import ServicePage
from tbx.taxonomy.models import Service
from tbx.work.models import WorkPage

from .streamfield import StreamFieldSerialiser


class PageInterface(graphene.Interface):
    title = graphene.String()
    slug = graphene.String()


class StreamField(Scalar):
    @staticmethod
    def serialize(val):
        return StreamFieldSerialiser().serialise_stream_block(val)


class ImageRenditionObjectType(graphene.ObjectType):
    url = graphene.String()
    width = graphene.Int()
    height = graphene.Int()


class ImageObjectType(graphene.ObjectType):
    FORMATS = {
        'quarter': 'width-400',  # Used by aligned image when alignment is either "left" or "right"
        'half': 'width-800',  # Used by aligned image when alignment is "half"
        'full': 'width-1280',  # Used by aligned image when alignment is "full"
        'logo': 'max-250x80',  # Used by logo block
        'icon': 'fill-100x100',
    }

    id = graphene.Int()
    alt = graphene.String()
    rendition = graphene.Field(ImageRenditionObjectType, format=graphene.String())
    width = graphene.Int()
    height = graphene.Int()

    def resolve_alt(self, info):
        return self.title

    def resolve_rendition(self, info, format):
        if format in ImageObjectType.FORMATS:
            return self.get_rendition(ImageObjectType.FORMATS[format])

        # TODO: Error


class ServiceObjectType(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()


class PersonPageObjectType(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    role = graphene.String()
    intro = graphene.String()
    biography = graphene.String()
    image = graphene.Field(ImageObjectType)

    class Meta:
        interfaces = [PageInterface]


class AuthorObjectType(graphene.ObjectType):
    name = graphene.String()
    role = graphene.String()
    image = graphene.Field(ImageObjectType)
    person_page = graphene.Field(PersonPageObjectType)


class ContactObjectType(graphene.ObjectType):
    name = graphene.String()
    role = graphene.String()
    image = graphene.Field(ImageObjectType)
    email_address = graphene.String()
    phone_number = graphene.String()


class BlogPostObjectType(graphene.ObjectType):
    body = StreamField()
    body_word_count = graphene.Int()
    authors = graphene.List(AuthorObjectType)
    date = graphene.Date()
    feed_image = graphene.Field(ImageObjectType)
    listing_summary = graphene.String()
    related_services = graphene.List(ServiceObjectType)

    def resolve_authors(self, info):
        return Author.objects.filter(
            id__in=self.authors.values_list('author_id', flat=True)
        )

    def resolve_related_services(self, info):
        return self.related_services.all()

    class Meta:
        interfaces = [PageInterface]


class CaseStudyObjectType(graphene.ObjectType):
    body = StreamField()
    body_word_count = graphene.Int()
    authors = graphene.List(AuthorObjectType)
    feed_image = graphene.Field(ImageObjectType)
    listing_summary = graphene.String()
    related_services = graphene.List(ServiceObjectType)

    def resolve_authors(self, info):
        return Author.objects.filter(
            id__in=self.authors.values_list('author_id', flat=True)
        )

    def resolve_related_services(self, info):
        return self.related_services.all()

    class Meta:
        interfaces = [PageInterface]


class ServicePageKeyPointObjectType(graphene.ObjectType):
    text = graphene.String()


class ServicePageClientLogoObjectType(graphene.ObjectType):
    image = graphene.Field(ImageObjectType)


class ServicePageTestimonialObjectType(graphene.ObjectType):
    quote = graphene.String()
    name = graphene.String()
    role = graphene.String()


class ServicePageObjectType(graphene.ObjectType):
    service = graphene.Field(ServiceObjectType)
    strapline = graphene.String()
    intro = graphene.String()
    heading_for_key_points = graphene.String()
    key_points = graphene.List(ServicePageKeyPointObjectType)
    contact = graphene.Field(ContactObjectType)
    client_logos = graphene.List(ServicePageClientLogoObjectType)
    usa_client_logos = graphene.List(ServicePageClientLogoObjectType)
    testimonials = graphene.List(ServicePageTestimonialObjectType)
    case_studies = graphene.List(CaseStudyObjectType)
    blog_posts = graphene.List(BlogPostObjectType)

    def resolve_key_points(self, info):
        return self.key_points.all()

    def resolve_client_logos(self, info):
        return self.client_logos.all()

    def resolve_usa_client_logos(self, info):
        return self.usa_client_logos.all()

    def resolve_testimonials(self, info):
        return self.testimonials.all()

    def resolve_case_studies(self, info):
        # TODO
        return []

    def resolve_blog_posts(self, info):
        # TODO
        return []

    class Meta:
        interfaces = [PageInterface]


class Query(graphene.ObjectType):
    services = graphene.List(ServiceObjectType, slug=graphene.String())
    person_pages = graphene.List(PersonPageObjectType, slug=graphene.String())
    blog_posts = graphene.List(BlogPostObjectType, slug=graphene.String(), service_slug=graphene.String())
    case_studies = graphene.List(CaseStudyObjectType, slug=graphene.String(), service_slug=graphene.String())
    service_pages = graphene.List(ServicePageObjectType, service_slug=graphene.String())
    images = graphene.List(ImageObjectType, ids=graphene.List(graphene.Int))

    def resolve_services(self, info, **kwargs):
        services = Service.objects.all().order_by('sort_order')

        if 'slug' in kwargs:
            services = services.filter(slug=kwargs['slug'])

        return services

    def resolve_service_pages(self, info, **kwargs):
        service_pages = ServicePage.objects.live().public()

        if 'service_slug' in kwargs:
            service_pages = service_pages.filter(service__slug=kwargs['service_slug'])

        return service_pages

    def resolve_blog_posts(self, info, **kwargs):
        blog_pages = BlogPage.objects.live().public().order_by('-date')

        if 'slug' in kwargs:
            blog_pages = blog_pages.filter(slug=kwargs['slug'])

        if 'service_slug' in kwargs:
            blog_pages = blog_pages.filter(related_services__slug=kwargs['service_slug'])

        return blog_pages

    def resolve_case_studies(self, info, **kwargs):
        work_pages = WorkPage.objects.live().public().order_by('-first_published_at')

        if 'slug' in kwargs:
            work_pages = work_pages.filter(slug=kwargs['slug'])

        if 'service_slug' in kwargs:
            work_pages = work_pages.filter(related_services__slug=kwargs['service_slug'])


        return work_pages

    def resolve_person_pages(self, info, **kwargs):
        person_pages = PersonPage.objects.live().public().order_by('last_name', 'first_name')

        if 'slug' in kwargs:
            person_pages = person_pages.filter(slug=kwargs['slug'])

        return person_pages

    def resolve_images(self, info, **kwargs):
        images = TorchboxImage.objects.all()
        if 'ids' in kwargs:
            images = images.filter(id__in=kwargs['ids'])

        return images


schema = graphene.Schema(
    query=Query,
)
