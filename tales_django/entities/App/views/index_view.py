from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import (
    get_common_context,
    get_favorites_list_context,
    get_recents_context,
    get_tracks_list_context,
    get_user_tracks_context,
)


@check_locale_decorator
def index_view(request: HttpRequest):

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tracks_list_context(request),
        **get_user_tracks_context(request),
        **get_recents_context(request),
        'show_top_columns': True,
    }

    return render(
        request=request,
        template_name='tales_django/index.html.django',
        context=context,
    )


__all__ = ['index_view']
