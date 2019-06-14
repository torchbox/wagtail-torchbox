from bs4 import BeautifulSoup
from wagtail.core.models import Page
from wagtail.core.rich_text import RichText


def serialize_rich_text(source):
    # Convert raw pseudo-HTML RichText source to a soup object
    # so it can be manipulated.
    soup = BeautifulSoup(source, 'html5lib')

    # Add data required to generate page links in Gatsby.
    for anchor in soup.find_all('a'):
        if anchor.attrs.get('linktype', '') == 'page':
            try:
                pages = Page.objects.live().public()
                page = pages.get(pk=anchor.attrs['id']).specific
                page_type = page.__class__.__name__

                new_tag = soup.new_tag(
                    'a',
                    href=page.get_url(),

                    # Add dataset arguments to allow processing links on
                    # the front-end.
                    **{
                        'data-page-type': page_type,
                        'data-page-slug': page.slug,
                        'data-page-service-slug': getattr(
                            getattr(page, 'service', None), 'slug', None
                        )
                    }
                )
                new_tag.append(*anchor.contents)
                anchor.replace_with(new_tag)
            except Page.DoesNotExist:
                # If page does not exist, add empty anchor tag with text.
                new_tag = soup.new_tag('a')
                new_tag.append(*anchor.contents)
                anchor.replace_with(new_tag)

    # Convert raw pseudo-HTML RichText into a front-end RichText
    return str(RichText(str(soup)))
