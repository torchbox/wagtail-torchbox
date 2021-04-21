from pattern_library.monkey_utils import override_tag

from tbx.people.templatetags.people_tags import register

override_tag(register, name="instagrampost")
