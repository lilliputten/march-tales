from django.conf import settings
from typing import List
from translated_fields import TranslatedField, to_attribute

from .get_currrent_django_language import get_currrent_django_language


def get_non_empty_localized_model_field_value(obj: object, name: str):
    """
    Get first non-empty alternative translation for the field if the current translaiton is empty
    """
    languages_list: List[str] = settings.LANGUAGES_LIST
    language = get_currrent_django_language()
    field_id = to_attribute(name, language)   # f'{name}_{language}'
    value = getattr(obj, field_id)
    if not value:
        # Try to find another translation...
        for lang in languages_list:
            if lang != language:
                field_id = to_attribute(name, lang)   # f'{name}_{lang}'
                value = getattr(obj, field_id)
                if value:
                    break
    return value


def get_non_empty_localized_model_field_attrgetter(name: str, field: TranslatedField):
    def getter(self):
        return get_non_empty_localized_model_field_value(self, name)

    return getter
