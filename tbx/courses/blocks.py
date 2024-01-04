from tbx.core import blocks as tbx_blocks
from wagtail import blocks


class CourseOutlineItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()


class CourseOutlineBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    course_outline = blocks.ListBlock(
        CourseOutlineItemBlock(),
    )

    class Meta:
        template = ("patterns/molecules/streamfield/blocks/course_outline_block.html",)


class ExternalLinkCTABlock(blocks.StructBlock):
    link_url = blocks.URLBlock(label="External Link")
    heading = blocks.CharBlock()
    text = blocks.CharBlock()

    class Meta:
        template = (
            "patterns/molecules/streamfield/blocks/external_link_cta_block.html",
        )


class CourseDetailStoryBlock(tbx_blocks.StoryBlock):
    course_outline = CourseOutlineBlock()
    external_link_cta = ExternalLinkCTABlock()
