from tbx.images.models import CustomImage
from wagtail_factories import ImageFactory


class CustomImageFactory(ImageFactory):
    class Meta:
        model = CustomImage
