from django.http import HttpRequest
from django.shortcuts import render

# from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.model_helpers import check_required_locale
from tales_django.core.pages import (
    get_common_context,
    get_favorites_list_context,
    # get_tracks_list_context,
)


logger = getDebugLogger()


def favorites_view(request: HttpRequest):

    check_required_locale(request)

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        # **get_tracks_list_context(request),
    }

    # debugData = {
    #     'language': language,
    #     'request': request,
    #     'context': context,
    #     # 'author_tracks': author_tracks,
    #     # 'author_tracks_offset': author_tracks_offset,
    # }
    # debugStr = debugObj(debugData)
    # logger.info(f'get_author_tracks_list_context\n{debugStr}')

    return render(
        request=request,
        template_name='tales_django/favorites.html.django',
        context=context,
    )


__all__ = ['favorites_view']
