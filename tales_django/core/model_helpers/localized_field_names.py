from django.conf import settings

from .localized_field_name import localized_field_name


def localized_field_names(prefix: str) -> list[str]:
    return list(map(lambda lang: localized_field_name(prefix, lang), settings.LANGUAGES_LIST))
