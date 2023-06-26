from datetime import timedelta

from django import template

from bs4 import BeautifulSoup
from tbx.core.blocks import ImageBlock

register = template.Library()

# Using value of 275 words per minute.
# https://help.medium.com/hc/en-us/articles/214991667-Read-time
WORDS_PER_SECOND = 275 / 60

# Every image adds 10 seconds.
SECONDS_PER_IMAGE = 10


@register.simple_tag(takes_context=True)
def get_reading_time_minutes(context, page, streamfield_name):
    """
    Calculate reading time of a `streamfield_name` on a `page`.

    Use streamfield stripped HTML and use their word count.
    Go through all image blocks to calculate approximate reading time.
    """
    total_seconds = 0

    page._reading_time = getattr(page, "_reading_time", {})

    reading_time = page._reading_time.get(streamfield_name)
    if not reading_time:
        # Streamfield value in HTML
        content_stream_value = getattr(page, streamfield_name)
        html_content = content_stream_value.render_as_block(context=context.flatten())

        # Strip all the HTML tags
        soup = BeautifulSoup(str(html_content), "html5lib")
        stripped_value = soup.text

        try:
            word_count = len(str(stripped_value).split())
            total_seconds += word_count / WORDS_PER_SECOND
        except ValueError:
            pass

        for block in content_stream_value:
            # Images
            if isinstance(block.block, ImageBlock):
                total_seconds += SECONDS_PER_IMAGE

        reading_time = timedelta(seconds=total_seconds)

        # Cache on a page instance to allow multiple calls
        page._reading_time[streamfield_name] = reading_time

    # Convert seconds to minutes
    reading_time_minutes = int(round(reading_time.seconds / 60))
    if reading_time_minutes <= 0:
        reading_time_minutes = 1

    return reading_time_minutes
