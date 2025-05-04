from django.conf import settings


def localized_field_name(prefix: str, lang: str) -> str:
    if not prefix.endswith('_'):
        prefix += '_'
    return prefix + lang
