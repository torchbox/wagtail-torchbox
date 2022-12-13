from tbx.core.blocks import CharBlock, RichTextBlock, StoryBlock
from wagtail.blocks import StructBlock
from wagtail.images.blocks import ImageChooserBlock


class ImpactReportHeadingBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    short_heading = CharBlock(required=False)
    heading = CharBlock(required=False)

    class Meta:
        icon = "title"
        template = (
            "patterns/molecules/streamfield/blocks/impact_report_heading_block.html",
        )


class ParagraphWithQuoteBlock(StructBlock):
    text = RichTextBlock()
    quote = CharBlock()
    attribution = CharBlock(required=False)

    class Meta:
        icon = "pilcrow"
        template = (
            "patterns/molecules/streamfield/blocks/paragraph_with_quote_block.html",
        )


class TextGridItemBlock(StructBlock):
    pass


class TextGridBlock(StructBlock):
    pass


class ImpactReportStoryBlock(StoryBlock):
    impact_report_heading = ImpactReportHeadingBlock()
    paragraph_with_quote_block = ParagraphWithQuoteBlock()
