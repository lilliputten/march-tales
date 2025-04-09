from django.conf import settings
from django.utils import translation


def get_current_language():
    language = translation.get_language()
    return language if language else settings.DEFAULT_LANGUAGE
