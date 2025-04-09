import re

from django.conf import settings


def get_valid_language(lang: str):
    lang = re.sub(r'^([A-Za-z]+).*$', r'\1', lang).lower()
    if lang not in settings.LANGUAGES_LIST:
        return settings.DEFAULT_LANGUAGE
    return lang
