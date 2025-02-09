from django.utils import translation

from django.conf import settings


def get_currrent_django_language():
    language = translation.get_language()
    return language if language else settings.DEFAULT_LANGUAGE
