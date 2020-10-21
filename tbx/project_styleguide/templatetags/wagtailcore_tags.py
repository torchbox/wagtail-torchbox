from wagtail.core.templatetags.wagtailcore_tags import register

from pattern_library.monkey_utils import override_tag

override_tag(register, name="include_block")
override_tag(register, name="pageurl")
override_tag(register, name="slugurl")
