from wagtail.images import get_image_model_string

import factory
from factory.django import DjangoModelFactory, ImageField


class ImageFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: "image_%d" % n)
    file = ImageField()

    class Meta:
        model = get_image_model_string()
