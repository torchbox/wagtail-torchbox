from django.conf import settings

from bs4 import BeautifulSoup
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.rich_text import RichText
from wagtail.embeds.blocks import EmbedBlock
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException
from wagtail.images.blocks import ImageChooserBlock


class StreamFieldSerialiser:
    def serialise_struct_block(self, block, value):
        blocks = {}
        for field_name, value in value.items():
            child_block = block.child_blocks[field_name]
            blocks[field_name] = self.serialise_block(child_block, value)

        return blocks

    def serialise_list_block(self, block, value):
        blocks = []
        for child_value in value:
            blocks.append(self.serialise_block(block.child_block, child_value))

        return blocks

    def serialise_stream_block(self, value):
        blocks = []
        for child_block in value:
            blocks.append({
                'type': child_block.block_type,
                'value': self.serialise_block(child_block.block, child_block.value),
            })

        return blocks

    def serialise_block(self, block, value):
        if hasattr(block, 'to_graphql_representation'):
            return block.to_graphql_representation(value)
        elif isinstance(block, blocks.RichTextBlock):
            return self.serialize_rich_text(value.source)
        elif isinstance(block, EmbedBlock):
            try:
                embed = get_embed(value.url)
                return {
                    'html': embed.html,
                    'url': value.url,
                }
            except EmbedException:
                return {
                    'html': '',
                    'url': None
                }
        elif isinstance(block, ImageChooserBlock):
            # FIXME
            return {
                'id': value.id,
                'alt': value.title,
                'src': settings.MEDIA_PREFIX + value.file.url,
                'hash': value.get_file_hash()
            }
        elif isinstance(block, blocks.FieldBlock):
            return value
        elif isinstance(block, blocks.StructBlock):
            return self.serialise_struct_block(block, value)
        elif isinstance(block, blocks.ListBlock):
            return self.serialise_list_block(block, value)
        elif isinstance(block, blocks.StreamBlock):
            return self.serialise_stream_block(block, value)

    def serialize_rich_text(self, source):
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
