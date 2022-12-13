from tbx.core.blocks import StoryBlock
from wagtail.blocks import CharBlock, ChoiceBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock


class ImpactReportHeadingBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    short_heading = CharBlock(required=False)
    heading = CharBlock(required=False)

    class Meta:
        icon = "title"
        template = (
            "patterns/molecules/streamfield/blocks/impact_report_heading_block.html"
        )


class ParagraphWithQuoteBlock(StructBlock):
    text = RichTextBlock()
    quote = CharBlock()
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
            "patterns/molecules/streamfield/blocks/paragraph_with_quote_block.html",
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


class ThreeColumnImageGrid(StructBlock):
    # 3 images with accompanying text
    pass


class DiagonalImageGrid(StructBlock):
    # 3 diagonally styled images
    pass


class TextGrid(StructBlock):
    # 2 columns of text with headings and images
    pass


class ImpactReportStoryBlock(StoryBlock):
    impact_report_heading = ImpactReportHeadingBlock()
    paragraph_with_quote = ParagraphWithQuoteBlock()
    paragraph_with_image = ParagraphWithImageBlock()
