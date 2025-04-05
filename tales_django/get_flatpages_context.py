from django.http import HttpRequest

from tales_django.core.pages import get_common_context
from tales_django.entities.flatpages.models import FlatPage


def get_flatpages_context(request: HttpRequest, flatpage: FlatPage):
    return get_common_context(request)
