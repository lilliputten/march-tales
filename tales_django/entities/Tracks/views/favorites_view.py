from django.http import HttpRequest
from django.shortcuts import render

# from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import (
    get_common_context,
    get_favorites_list_context,
    # get_tracks_list_context,
)


logger = getDebugLogger()


@check_locale_decorator
def favorites_view(request: HttpRequest):

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        # **get_tracks_list_context(request),
    }

    return render(
        request=request,
        template_name='tales_django/favorites.html.django',
        context=context,
    )


__all__ = ['favorites_view']
