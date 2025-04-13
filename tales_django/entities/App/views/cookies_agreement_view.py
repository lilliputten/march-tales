from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import (
    get_common_context,
    get_favorites_list_context,
    get_tracks_list_context,
    get_user_tracks_context,
)


@check_locale_decorator
def cookies_agreement_view(request: HttpRequest):

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tracks_list_context(request),
        **get_user_tracks_context(request),
    }
    return render(
        request=request,
        template_name='tales_django/cookies-agreement.html.django',
        context=context,
    )


__all__ = ['cookies_agreement_view']
