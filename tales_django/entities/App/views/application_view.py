from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.pages import get_common_context, get_favorites_list_context, get_tracks_list_context


def application_view(request: HttpRequest):
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tracks_list_context(request),
    }
    return render(
        request=request,
        template_name='tales_django/application.html.django',
        context=context,
    )


__all__ = ['application_view']
