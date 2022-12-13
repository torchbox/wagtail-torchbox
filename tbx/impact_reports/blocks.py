from tbx.core.blocks import CharBlock, StoryBlock
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


class ImpactReportStoryBlock(StoryBlock):
    impact_report_heading = ImpactReportHeadingBlock()
