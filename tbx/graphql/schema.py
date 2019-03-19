import graphene
from graphene.types import Scalar
from django.conf import settings

from tbx.blog.models import BlogPage, BlogIndexPage
from tbx.core.models import JobIndexPage, TorchboxImage, StandardPage, MainMenu
from tbx.people.models import Author, PersonIndexPage, PersonPage, CulturePage, Contact, ContactReasonsList
from tbx.services.models import ServicePage, SubServicePage
from tbx.taxonomy.models import Service
from tbx.work.models import WorkPage, WorkIndexPage

from .streamfield import StreamFieldSerialiser


class ImageRenditionObjectType(graphene.ObjectType):
    url = graphene.String()
    width = graphene.Int()
    height = graphene.Int()
    hash = graphene.String()
    alt = graphene.String()

    def resolve_url(self, info):
        return settings.MEDIA_PREFIX + self.file.url

    def resolve_hash(self, format):
        return self.image.get_file_hash()

    def resolve_alt(self, info):
        return self.title


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


class ContactReasonObjectType(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()


class ContactReasonsObjectType(graphene.ObjectType):
    name = graphene.String()
    heading = graphene.String()
    is_default = graphene.Boolean()
    reasons = graphene.List(ContactReasonObjectType)

    def resolve_reasons(self, info):
        return self.reasons.get_queryset()


def get_prioritised_service(self, info):
        if hasattr(self, 'related_services'):
            return self.related_services.order_by('sort_order').first()

        if hasattr(self, 'service'):
            return self.service

        return None


class PageInterface(graphene.Interface):
    title = graphene.String()
    page_title = graphene.String()
    search_description = graphene.String()
    slug = graphene.String()
    contact = graphene.Field(ContactObjectType)
    contact_reasons = graphene.Field(ContactReasonsObjectType)

    def resolve_page_title(self, info):
        title = ''
        if self.seo_title:
            title += self.seo_title
        else:
            title += self.title

        return title

    def resolve_search_description(self, info):
        description = self.title

        if hasattr(self, 'listing_summary'):
            if self.listing_summary:
                description = self.listing_summary

        if hasattr(self, 'search_description'):
            if self.search_description:
                description = self.search_description

        return description

    def resolve_contact(self, info):
        if hasattr(self, 'contact'):
            if self.contact is not None:
                return self.contact

        service = get_prioritised_service(self, info)
        if service is not None:
            if service.preferred_contact is not None:
                return service.preferred_contact

        try:
            return Contact.objects.get(default_contact=True)
        except:
            return None

    def resolve_contact_reasons(self, info):
        if hasattr(self, 'contact_reasons'):
            if self.contact_reasons is not None:
                return self.contact_reasons

        service = get_prioritised_service(self, info)
        if service is not None:
            if service.contact_reasons is not None:
                return service.contact_reasons

        try:
            return ContactReasonsList.objects.get(is_default=True)
        except:
            return None


class PageLink(graphene.ObjectType):
    type = graphene.String()
    slug = graphene.String()
    service_slug = graphene.String()

    def resolve_type(self, info):
        return self.specific.__class__.__name__

    def resolve_service_slug(self, info):
        if hasattr(self.specific, 'parent_service'):
            return self.specific.parent_service.slug


class StreamField(Scalar):
    @staticmethod
    def serialize(val):
        return StreamFieldSerialiser().serialise_stream_block(val)


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
            return Contact.objects.get(default_contact=True)

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


class BlogIndexPageObjectType(graphene.ObjectType):
    intro = graphene.String()

    class Meta:
        interfaces = [PageInterface]


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
        return self.related_services.order_by('sort_order').all()

    class Meta:
        interfaces = [PageInterface]


class CaseStudyIndexPageObjectType(graphene.ObjectType):
    intro = graphene.String()

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

    def resolve_page_link_label(self, info):
        if self.page_link is not None:
            if self.page_link_label is "":
                return self.page_link.title
            return self.page_link_label
        return ""


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

    def resolve_parent_service(self, info):
        if hasattr(self, 'parent_service'):
            return self.parent_service
        return None

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
    strapline = graphene.String()

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
    links = graphene.List(CulturePageLinkObjectType)

    def resolve_links(self, info):
        return self.links.all()

    class Meta:
        interfaces = [PageInterface]


def get_page_revision(page, revision_id):
        revision = page.revisions.filter(id=revision_id).first()
        if revision:
            page = revision.as_page_object()
            page.revision = revision.id
            return page
        return None


class Query(graphene.ObjectType):
    # Service Snippets
    service = graphene.Field(ServiceObjectType, slug=graphene.String())
    services = graphene.List(ServiceObjectType)
    # Person Pages
    person_page = graphene.Field(PersonPageObjectType, slug=graphene.String(), revision=graphene.String())
    person_pages = graphene.List(PersonPageObjectType)
    person_index_page = graphene.Field(PersonIndexPageObjectType, revision=graphene.String())
    # Blog Posts
    blog_post = graphene.Field(BlogPostObjectType, slug=graphene.String(), revision=graphene.String() )
    blog_posts = graphene.List(BlogPostObjectType, service_slug=graphene.String(), author_slug=graphene.String(), limit=graphene.Int())
    blog_index_page = graphene.Field(BlogIndexPageObjectType, revision=graphene.String())
    # Case-Study / Work Pages
    case_study = graphene.Field(CaseStudyObjectType, slug=graphene.String(), revision=graphene.String() )
    case_studies = graphene.List(CaseStudyObjectType, slug=graphene.String(), service_slug=graphene.String(), limit=graphene.Int())
    case_study_index_page = graphene.Field(CaseStudyIndexPageObjectType, revision=graphene.String())
    # Service Pages
    service_page = graphene.Field(ServicePageObjectType, service_slug=graphene.String(), revision=graphene.String())
    service_pages = graphene.List(ServicePageObjectType)
    # Sub-services Pages
    sub_service_page = graphene.Field(ServicePageObjectType, slug=graphene.String(), revision=graphene.String())
    sub_service_pages = graphene.List(ServicePageObjectType, slug=graphene.String(), service_slug=graphene.String())
    # Standard Pages
    standard_page = graphene.Field(StandardPageObjectType, slug=graphene.String(), revision=graphene.String())
    standard_pages = graphene.List(StandardPageObjectType)
    # Jobs pages
    jobs_index_page = graphene.Field(JobsIndexPageObjectType, revision=graphene.String())
    # Culture Pages
    culture_page = graphene.Field(CulturePageObjectType, slug=graphene.String(), revision=graphene.String())
    culture_pages = graphene.List(CulturePageObjectType)
    # Images
    images = graphene.List(ImageObjectType, ids=graphene.List(graphene.Int))
    # Contact fields
    contact = graphene.Field(ContactObjectType)
    contact_reasons = graphene.Field(ContactReasonsObjectType)

    def resolve_service(self, info, slug, **kwargs):
        if slug:
            return Service.objects.first(slug=slug)

        return None

    def resolve_services(self, info, **kwargs):
        return Service.objects.all().order_by('sort_order')

    def resolve_person_page(self, info, slug, **kwargs):
            if slug:
                person_page = PersonPage.objects.filter(slug=slug).first()

            if 'revision' in kwargs:
                person_page = get_page_revision(person_page, kwargs['revision'])

            return person_page

    def resolve_person_pages(self, info, **kwargs):
        return PersonPage.objects.live().public().order_by('last_name', 'first_name')

    def resolve_service_page(self, info, service_slug, **kwargs):            
        if service_slug:
            service_page = ServicePage.objects.filter(service__slug=service_slug).first()

        if 'revision' in kwargs:
            service_page = get_page_revision(service_page, kwargs['revision'])

        return service_page
    
    def resolve_service_pages(self, info, **kwargs):
        return ServicePage.objects.live().public()

    def resolve_sub_service_page(self, info, slug, **kwargs):
        if slug:
            sub_service_page = SubServicePage.objects.filter(slug=slug).first()

        if 'revision' in kwargs:
            sub_service_page = get_page_revision(sub_service_page, kwargs['revision'])

        return sub_service_page

    def resolve_sub_service_pages(self, info, **kwargs):
        return SubServicePage.objects.live().public()

    def resolve_blog_post(self, info, slug, **kwargs):
        if slug:
            blog_page = BlogPage.objects.filter(slug=slug).first()

        if 'revision' in kwargs:
            blog_page = get_page_revision(blog_page, kwargs['revision'])

        return blog_page

    def resolve_blog_posts(self, info, **kwargs):
        blog_pages = BlogPage.objects.live().public().order_by('-date')

        if 'service_slug' in kwargs:
            blog_pages = blog_pages.filter(related_services__slug=kwargs['service_slug'])

        if 'author_slug' in kwargs:
            blog_pages = blog_pages.filter(authors__author__person_page__slug=kwargs['author_slug'])

        if 'limit' in kwargs:
            blog_pages = blog_pages.order_by("-date")[:kwargs['limit']]

        return blog_pages

    def resolve_blog_index_page(self, info, **kwargs):
        index_page = BlogIndexPage.objects.first()

        if 'revision' in kwargs:
            index_page = get_page_revision(index_page, kwargs['revision'])

        return index_page


    def resolve_case_study(self, info, slug, **kwargs):
        if slug:
            work_page = WorkPage.objects.filter(slug=slug).first()

        if 'revision' in kwargs:
            work_page = get_page_revision(work_page, kwargs['revision'])

        return work_page

    def resolve_case_studies(self, info, **kwargs):
        work_pages = WorkPage.objects.live().public().order_by('-first_published_at')

        if 'service_slug' in kwargs:
            work_pages = work_pages.filter(related_services__slug=kwargs['service_slug'])

        return work_pages

    def resolve_case_study_index_page(self, info, **kwargs):
        index_page = WorkIndexPage.objects.first()

        if 'revision' in kwargs:
            index_page = get_page_revision(index_page, kwargs['revision'])

        return index_page
    
    def resolve_standard_page(self, info, slug, **kwargs):
        if slug:
            standard_page = StandardPage.objects.filter(slug=slug).first()

        if 'revision' in kwargs:
            standard_page = get_page_revision(standard_page, kwargs['revision'])

        return standard_page

    def resolve_standard_pages(self, info, **kwargs):
        return StandardPage.objects.live().public().order_by('title')

    def resolve_jobs_index_page(self, info, **kwargs):
        jobs_page = JobIndexPage.objects.live().public().first()

        if 'revision' in kwargs:
            jobs_page = get_page_revision(jobs_page, kwargs['revision'])

        return jobs_page

    def resolve_person_index_page(self, info, **kwargs):
        persons_page = PersonIndexPage.objects.live().public().first()

        if 'revision' in kwargs:
            persons_page = get_page_revision(persons_page, kwargs['revision'])

        return persons_page

    def resolve_culture_page(self, info, slug, **kwargs):
        if slug:
            culture_page = CulturePage.objects.filter(slug=slug).first()

        if 'revision' in kwargs:
            culture_page = get_page_revision(culture_page, kwargs['revision'])

        return culture_page
    
    def resolve_culture_pages(self, info, **kwargs):
        return CulturePage.objects.live().public()

    def resolve_images(self, info, **kwargs):
        images = TorchboxImage.objects.all()
        if 'ids' in kwargs:
            images = images.filter(id__in=kwargs['ids'])

        return images

    def resolve_contact(self, info):
        try:
            return Contact.objects.get(default_contact=True)
        except:
            return None

    def resolve_contact_reasons(self, info):
        try:
            return ContactReasonsList.objects.get(is_default=True)
        except:
            return None


schema = graphene.Schema(
    query=Query,
)
