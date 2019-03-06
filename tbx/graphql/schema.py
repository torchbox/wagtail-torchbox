import graphene
from graphene.types import Scalar
from django.conf import settings

from tbx.blog.models import BlogPage
from tbx.core.models import JobIndexPage, TorchboxImage, StandardPage, MainMenu
from tbx.people.models import Author, PersonIndexPage, PersonPage, CulturePage, Contact
from tbx.services.models import ServicePage, SubServicePage
from tbx.taxonomy.models import Service
from tbx.work.models import WorkPage

from .streamfield import StreamFieldSerialiser


class PageInterface(graphene.Interface):
    title = graphene.String()
    page_title = graphene.String()
    slug = graphene.String()

    def resolve_page_title(self, info):
        title = ''
        if self.seo_title:
            title += self.seo_title
        else:
            title += self.title

        return title


class PageLink(graphene.ObjectType):
    type = graphene.String()
    slug = graphene.String()

    def resolve_type(self, info):
        return self.specific.__class__.__name__


class StreamField(Scalar):
    @staticmethod
    def serialize(val):
        return StreamFieldSerialiser().serialise_stream_block(val)


class ImageRenditionObjectType(graphene.ObjectType):
    url = graphene.String()
    width = graphene.Int()
    height = graphene.Int()
    hash = graphene.String()

    def resolve_url(self, info):
        return settings.MEDIA_PREFIX + self.file.url

    def resolve_hash(self, format):
        return self.image.get_file_hash()


class ImageObjectType(graphene.ObjectType):
    FORMATS = {
        'quarter': 'width-400',  # Used by aligned image when alignment is either "left" or "right"
        'half': 'width-800',  # Used by aligned image when alignment is "half"
        'full': 'width-1280',
        'max': 'width-1920',
        'logo': 'max-250x80',  # Used by logo block
        'icon': 'fill-100x100',
        'large-icon': 'fill-400x400',
    }

    id = graphene.Int()
    src = graphene.String()
    alt = graphene.String()
    hash = graphene.String()
    rendition = graphene.Field(ImageRenditionObjectType, format=graphene.String())
    width = graphene.Int()
    height = graphene.Int()

    def resolve_alt(self, info):
        return self.title

    def resolve_src(self, info):
        return settings.MEDIA_PREFIX + self.file.url

    def resolve_hash(self, info):
        return self.get_file_hash()

    def resolve_rendition(self, info, format):
        if format in ImageObjectType.FORMATS:
            return self.get_rendition(ImageObjectType.FORMATS[format])

        # TODO: Error


class ContactObjectType(graphene.ObjectType):
    name = graphene.String()
    role = graphene.String()
    image = graphene.Field(ImageObjectType)
    email_address = graphene.String()
    phone_number = graphene.String()


class ServiceObjectType(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    description = graphene.String()
    service_page = graphene.Field(PageLink)
    preferred_contact = graphene.Field(ContactObjectType)

    def resolve_service_page(self, info):
        service_pages = ServicePage.objects.live().public()
        service_pages = service_pages.filter(service__slug=self.slug)
        if len(service_pages):
            return service_pages.filter(service__slug=self.slug)[0]
        return None

    def resolve_preferred_contact(self, info):
        if self.preferred_contact is None:
            return Contact.objects.first()

        return self.preferred_contact


class PersonPageObjectType(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    short_intro = graphene.String()
    alt_short_intro = graphene.String()
    role = graphene.String()
    intro = graphene.String()
    biography = graphene.String()
    image = graphene.Field(ImageObjectType)
    is_senior = graphene.Boolean()

    class Meta:
        interfaces = [PageInterface]

    def resolve_is_senior(self, info):
        return self.is_senior


class AuthorObjectType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    role = graphene.String()
    image = graphene.Field(ImageObjectType)
    person_page = graphene.Field(PersonPageObjectType)


class BlogPostObjectType(graphene.ObjectType):
    body = StreamField()
    body_word_count = graphene.Int()
    authors = graphene.List(AuthorObjectType)
    date = graphene.Date()
    feed_image = graphene.Field(ImageObjectType)
    listing_summary = graphene.String()
    related_services = graphene.List(ServiceObjectType)
    contact = graphene.Field(ContactObjectType)

    def resolve_authors(self, info):
        return Author.objects.filter(
            id__in=self.authors.values_list('author_id', flat=True)
        )

    def resolve_related_services(self, info):
        return self.related_services.order_by('sort_order').all()

    def resolve_contact(self, info):
        service = self.related_services.order_by('sort_order').first()
        if service is not None:
            if service.preferred_contact is not None:
                return service.preferred_contact
        return Contact.objects.get(default_contact=True)

    class Meta:
        interfaces = [PageInterface]


class CaseStudyObjectType(graphene.ObjectType):
    body = StreamField()
    client = graphene.String()
    body_word_count = graphene.Int()
    authors = graphene.List(AuthorObjectType)
    feed_image = graphene.Field(ImageObjectType)
    homepage_image = graphene.Field(ImageObjectType)
    listing_summary = graphene.String()
    related_services = graphene.List(ServiceObjectType)
    contact = graphene.Field(ContactObjectType)

    def resolve_authors(self, info):
        return Author.objects.filter(
            id__in=self.authors.values_list('author_id', flat=True)
        )

    def resolve_related_services(self, info):
        return self.related_services.all()

    def resolve_contact(self, info):
        service = self.related_services.order_by('sort_order').first()
        if service is not None:
            if service.preferred_contact is not None:
                return service.preferred_contact
        return Contact.objects.get(default_contact=True)

    class Meta:
        interfaces = [PageInterface]


class ServicePageKeyPointObjectType(graphene.ObjectType):
    text = graphene.String()
    linked_page = graphene.Field(PageLink)


class ServicePageClientLogoObjectType(graphene.ObjectType):
    image = graphene.Field(ImageObjectType)


class ServicePageTestimonialObjectType(graphene.ObjectType):
    quote = graphene.String()
    name = graphene.String()
    role = graphene.String()


class ProcessObjectType(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    page_link = graphene.Field(PageLink)
    page_link_label = graphene.String()


class ServicePageObjectType(graphene.ObjectType):
    parent_service = graphene.Field(ServiceObjectType)
    service = graphene.Field(ServiceObjectType)
    is_darktheme = graphene.Boolean()

    strapline = graphene.String()
    intro = graphene.String()
    greeting_image_type = graphene.String()

    key_points_section_title = graphene.String()
    heading_for_key_points = graphene.String()
    key_points = graphene.List(ServicePageKeyPointObjectType)

    contact = graphene.Field(ContactObjectType)

    process_section_title = graphene.String()
    heading_for_processes = graphene.String()
    use_process_block_image = graphene.Boolean()
    processes = graphene.List(ProcessObjectType)

    testimonials_section_title = graphene.String()
    client_logos = graphene.List(ServicePageClientLogoObjectType)
    usa_client_logos = graphene.List(ServicePageClientLogoObjectType)
    testimonials = graphene.List(ServicePageTestimonialObjectType)

    blogs_section_title = graphene.String()
    blog_posts = graphene.List(BlogPostObjectType, limit=graphene.Int())
    case_studies_section_title = graphene.String()
    case_studies = graphene.List(CaseStudyObjectType, limit=graphene.Int())

    def resolve_key_points(self, info):
        return self.key_points.all()

    def resolve_client_logos(self, info):
        return self.client_logos.all()

    def resolve_usa_client_logos(self, info):
        return self.usa_client_logos.all()

    def resolve_testimonials(self, info):
        return self.testimonials.all()

    def resolve_processes(self, info):
        return self.processes.all()

    def resolve_blog_posts(self, info, **kwargs):
        limit = kwargs.get('limit', 10)
        blog_pages = BlogPage.objects.live().public()

        # Get featured in same order as in the editor
        featured_ids = list(self.featured_blog_posts.values_list('blog_post_id', flat=True)[:limit])
        featured_pages = blog_pages.in_bulk(featured_ids)
        featured = [
            featured_pages[featured_id]
            for featured_id in featured_ids
        ]

        if self.service is not None:
            blog_pages = blog_pages.filter(related_services__slug=self.service.slug)
            if len(blog_pages) == 0:
                return None

        # Get additional work pages
        num_additional_required = limit - len(featured)
        additional = list(blog_pages.exclude(id__in=featured_ids).order_by('-date')[:num_additional_required])

        return featured + additional

    def resolve_case_studies(self, info, **kwargs):
        limit = kwargs.get('limit', 10)
        work_pages = WorkPage.objects.live().public()

        # Get featured in same order as in the editor
        featured_ids = list(self.featured_case_studies.values_list('case_study_id', flat=True)[:limit])
        featured_pages = work_pages.in_bulk(featured_ids)
        featured = [
            featured_pages[featured_id]
            for featured_id in featured_ids
        ]

        if self.service is not None:
            work_pages = work_pages.filter(related_services__slug=self.service.slug)
            if len(work_pages) == 0:
                return None

        # Get additional work pages
        num_additional_required = limit - len(featured)
        additional = list(
            work_pages.exclude(id__in=featured_ids).order_by('-first_published_at')[:num_additional_required])

        return featured + additional

    class Meta:
        interfaces = [PageInterface]


class StandardPageObjectType(graphene.ObjectType):
    body = StreamField()

    class Meta:
        interfaces = [PageInterface]


class JobsIndexPageJob(graphene.ObjectType):
    title = graphene.String()
    level = graphene.String()
    location = graphene.String()
    url = graphene.String()


class JobsIndexPageObjectType(graphene.ObjectType):
    jobs = graphene.List(JobsIndexPageJob)

    def resolve_jobs(self, info):
        return self.jobs.all()

    class Meta:
        interfaces = [PageInterface]


class PersonIndexPageObjectType(graphene.ObjectType):
    strapline = graphene.String()

    class Meta:
        interfaces = [PageInterface]


class CulturePageLinkObjectType(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    link = graphene.Field(PageLink)


class CulturePageObjectType(graphene.ObjectType):
    strapline = graphene.String()
    hero_image = graphene.Field(ImageObjectType)
    intro = graphene.String()
    body = graphene.Field(StreamField)
    contact = graphene.Field(ContactObjectType)
    links = graphene.List(CulturePageLinkObjectType)

    def resolve_links(self, info):
        return self.links.all()

    class Meta:
        interfaces = [PageInterface]


class Query(graphene.ObjectType):
    services = graphene.List(ServiceObjectType, slug=graphene.String())
    person_pages = graphene.List(PersonPageObjectType, slug=graphene.String())
    blog_posts = graphene.List(BlogPostObjectType, slug=graphene.String(), service_slug=graphene.String(),
                               author_slug=graphene.String(), limit=graphene.Int())
    case_studies = graphene.List(CaseStudyObjectType, slug=graphene.String(), service_slug=graphene.String(), limit=graphene.Int())
    services = graphene.List(ServiceObjectType, slug=graphene.String())
    service_pages = graphene.List(ServicePageObjectType, service_slug=graphene.String())
    sub_service_pages = graphene.List(ServicePageObjectType, slug=graphene.String(), service_slug=graphene.String())
    standard_pages = graphene.List(StandardPageObjectType, slug=graphene.String())
    jobs_index_page = graphene.Field(JobsIndexPageObjectType)
    person_index_page = graphene.Field(PersonIndexPageObjectType)
    culture_pages = graphene.List(CulturePageObjectType, slug=graphene.String())
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

    def resolve_sub_service_pages(self, info, **kwargs):
        sub_service_pages = SubServicePage.objects.live().public()

        if 'slug' in kwargs:
            sub_service_pages = sub_service_pages.filter(slug=kwargs['slug'])

        if 'service_slug' in kwargs:
            sub_service_pages = sub_service_pages.filter(service__slug=kwargs['service_slug'])

        return sub_service_pages

    def resolve_blog_posts(self, info, **kwargs):
        blog_pages = BlogPage.objects.live().public().order_by('-date')

        if 'slug' in kwargs:
            blog_pages = blog_pages.filter(slug=kwargs['slug'])

        if 'service_slug' in kwargs:
            blog_pages = blog_pages.filter(related_services__slug=kwargs['service_slug'])

        if 'author_slug' in kwargs:
            blog_pages = blog_pages.filter(authors__author__person_page__slug=kwargs['author_slug'])

        if 'limit' in kwargs:
            blog_pages = blog_pages.order_by("-date")[:kwargs['limit']]

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

    def resolve_standard_pages(self, info, **kwargs):
        standard_pages = StandardPage.objects.live().public().order_by('title')

        if 'slug' in kwargs:
            standard_pages = standard_pages.filter(slug=kwargs['slug'])

        return standard_pages

    def resolve_jobs_index_page(self, info):
        return JobIndexPage.objects.live().public().first()

    def resolve_person_index_page(self, info):
        return PersonIndexPage.objects.live().public().first()

    def resolve_culture_pages(self, info, **kwargs):
        culture_pages = CulturePage.objects.live().public()

        if 'slug' in kwargs:
            culture_pages = culture_pages.filter(slug=kwargs['slug'])

        return culture_pages

    def resolve_images(self, info, **kwargs):
        images = TorchboxImage.objects.all()
        if 'ids' in kwargs:
            images = images.filter(id__in=kwargs['ids'])

        return images


schema = graphene.Schema(
    query=Query,
)
