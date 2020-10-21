from wagtail.images.templatetags.wagtailimages_tags import register

from pattern_library.monkey_utils import override_tag

override_tag(register, name="image")
