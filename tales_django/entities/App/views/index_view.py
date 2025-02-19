from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.pages import get_common_context, get_tracks_list_context


def index_view(request: HttpRequest):
    context = {
        **get_common_context(request),
        **get_tracks_list_context(request),
    }

    return render(
        request=request,
        template_name='tales_django/index.html.django',
        context=context,
    )


__all__ = ['index_view']
