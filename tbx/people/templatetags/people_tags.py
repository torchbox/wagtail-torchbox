from django import template

from wagtail.embeds.models import Embed

register = template.Library()


@register.inclusion_tag("patterns/atoms/instagram-post/instagram-post.html")
def instagrampost(embed):
    return {"post": Embed.objects.get(url=embed.value.url)}
