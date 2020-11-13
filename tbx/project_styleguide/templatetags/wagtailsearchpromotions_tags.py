from pattern_library.monkey_utils import override_tag
from wagtail.contrib.search_promotions.templatetags.wagtailsearchpromotions_tags import (
    register,
)

override_tag(register, name="get_search_promotions")
