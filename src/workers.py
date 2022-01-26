import string
from random import choice


def generate_short_id(num_of_chars: int):

    return ''.join(
        choice(string.ascii_letters + string.digits) for _ in
        range(num_of_chars)
        )


def short_url_complexity(length, count=1):
    raw_length = length/72
    if raw_length < 72:
        return count+1
    return short_url_complexity(raw_length, count+1)
