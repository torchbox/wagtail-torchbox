import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

color_re = re.compile(r"^[A-Fa-f0-9]{6}$")
color_validator = RegexValidator(color_re, _("Enter a valid color."), "invalid")


class ColorField(models.CharField):
    default_validators = [color_validator]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        super(ColorField, self).__init__(*args, **kwargs)
