import re

_CLEANR = re.compile('<.*?>')


def remove_html_tags(s: str):
    return re.sub(_CLEANR, '', s)
