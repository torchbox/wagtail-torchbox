from pattern_library.monkey_utils import override_tag

from tbx.navigation.templatetags.navigation_tags import register

override_tag(register, name="primarynav")
override_tag(register, name="secondarynav")
override_tag(register, name="footernav")
override_tag(register, name="sidebar")
override_tag(register, name="footerlinks")
