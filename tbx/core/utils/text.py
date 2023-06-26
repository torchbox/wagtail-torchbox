import math
import string

from bs4 import BeautifulSoup


def get_word_count(text: str) -> int:
    body_text = BeautifulSoup(text, "html.parser").get_text()
    remove_chars = string.punctuation + "“”’"
    body_words = body_text.translate(
        body_text.maketrans(dict.fromkeys(remove_chars))
    ).split()
    return len(body_words)


def get_read_time(word_count: int) -> int:
    """
    Calculate how long it will take on average to read the page,
    given the number of words on it.
    """
    if word_count:
        return math.ceil(word_count / 275)
    else:
        return 0
