from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.pages import get_tracks_list_context


def terms_view(request: HttpRequest):
    return render(
        request=request,
        template_name='tales_django/terms.html.django',
        context=get_tracks_list_context(request),
    )


__all__ = ['terms_view']
