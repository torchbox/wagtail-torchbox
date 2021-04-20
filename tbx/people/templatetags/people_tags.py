from django import template

from wagtail.embeds.models import Embed

register = template.Library()


@register.inclusion_tag("patterns/atoms/instagram-post/instagram-post.html")
def include_instagram_post(embed):
    return {"post": Embed.objects.get(url=embed.value.url)}
