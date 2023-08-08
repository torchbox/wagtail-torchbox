from tbx.core.blocks import StoryBlock
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RichTextBlock,
    StructBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class ImpactReportHeadingBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    short_heading = CharBlock(
        required=False, help_text="Used for the Table of Contents"
    )
    heading = CharBlock(required=False)

    class Meta:
        icon = "title"
        template = (
            "patterns/molecules/streamfield/blocks/impact_report_heading_block.html"
        )


class ParagraphWithQuoteBlock(StructBlock):
    text = RichTextBlock()
    quote = RichTextBlock(features=["bold", "italic", "link", "document-link"])
    attribution = CharBlock(required=False)
    quote_alignment = ChoiceBlock(
        choices=[
            ("left", "Left"),
            ("right", "Right"),
        ],
        default="right",
    )

    class Meta:
        icon = "pilcrow"
        template = (
            "patterns/molecules/streamfield/blocks/paragraph_with_quote_block.html"
        )


class ParagraphWithImageBlock(StructBlock):
    text = RichTextBlock()
    image = ImageChooserBlock(required=False)
    image_alignment = ChoiceBlock(
        choices=[
            ("left", "Left"),
            ("right", "Right"),
        ],
        default="right",
    )

    class Meta:
        icon = "pilcrow"
        template = (
            "patterns/molecules/streamfield/blocks/paragraph_with_image_block.html"
        )


class ThreeColumnImageGridItemBlock(StructBlock):
    image = ImageChooserBlock()
    text = CharBlock()

    class Meta:
        icon = "image"


class ThreeColumnImageGridBlock(StructBlock):
    items = ListBlock(ThreeColumnImageGridItemBlock(), min_num=3, max_num=3)

    class Meta:
        icon = "image"
        template = (
            "patterns/molecules/streamfield/blocks/three_column_image_grid_block.html"
        )


class TwoColumnTextGridItemBlock(StructBlock):
    image = ImageChooserBlock()
    heading = CharBlock()
    text = CharBlock()


class TwoColumnTextGridBlock(StructBlock):
    items = ListBlock(TwoColumnTextGridItemBlock())

    class Meta:
        icon = "grip"
        template = (
            "patterns/molecules/streamfield/blocks/two_column_text_grid_block.html"
        )


class SmallImageWithTextBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock()
    text = RichTextBlock()

    class Meta:
        icon = "image"
        template = (
            "patterns/molecules/streamfield/blocks/small_image_with_text_block.html"
        )


class InstagramGalleryItemBlock(StructBlock):
    image = ImageChooserBlock()
    link = URLBlock(
        required=False,
    )

    class Meta:
        icon = "image"


class InstagramGalleryGridBlock(StructBlock):
    items = ListBlock(InstagramGalleryItemBlock())

    class Meta:
        icon = "group"
        template = "patterns/molecules/streamfield/blocks/instagram-gallery.html"


class ImpactReportStoryBlock(StoryBlock):
    impact_report_heading = ImpactReportHeadingBlock(group="Impact Report")
    paragraph_with_quote = ParagraphWithQuoteBlock(group="Impact Report")
    paragraph_with_image = ParagraphWithImageBlock(group="Impact Report")
    three_column_image_grid = ThreeColumnImageGridBlock(group="Impact Report")
    two_column_text_grid = TwoColumnTextGridBlock(group="Impact Report")
    small_image_with_text = SmallImageWithTextBlock(group="Impact Report")
    instagram_gallery = InstagramGalleryGridBlock(group="Impact Report")
