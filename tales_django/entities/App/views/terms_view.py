from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.pages import get_common_context, get_favorites_list_context, get_user_tracks_context


def terms_view(request: HttpRequest):
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_user_tracks_context(request),
        # **get_tracks_list_context(request),
    }
    return render(
        request=request,
        template_name='tales_django/terms.html.django',
        context=context,
    )


__all__ = ['terms_view']
