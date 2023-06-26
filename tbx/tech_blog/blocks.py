from typing import Iterator

from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import find_lexer_class, get_all_lexers
from tbx.core.blocks import StoryBlock
from wagtail.blocks import ChoiceBlock, StructBlock, StructValue, TextBlock


def get_language_choices() -> Iterator[tuple[str, str]]:
    for name, _, _, _ in sorted(get_all_lexers()):
        yield (name, name.replace("+", " + "))


class CodeStructValue(StructValue):
    def code(self) -> str:
        lexer = find_lexer_class(self["language"])()
        formatter = HtmlFormatter(linenos=None, noclasses=True)
        return mark_safe(highlight(self["source"], lexer, formatter))


class CodeBlock(StructBlock):
    language = ChoiceBlock(
        choices=get_language_choices,
    )
    source = TextBlock()

    class Meta:
        icon = "code"
        value_class = CodeStructValue
        template = "patterns/molecules/streamfield/blocks/code_block.html"


class TechBlogBlock(StoryBlock):
    """
    Blocks specific for the tech blog, to avoid polluting the rest of the site.
    """

    code = CodeBlock()
