from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from core.logging import getDebugLogger
from tales_django.core.model_helpers import check_required_locale
from tales_django.core.pages import get_author_tracks_list_context, get_common_context, get_favorites_list_context
from tales_django.entities.Tracks.models import Author


logger = getDebugLogger()


def author_details_view(request: HttpRequest, author_id):

    check_required_locale(request)

    author = get_object_or_404(Author, id=author_id)

    # TODO: Use get_generic_context (without authors list)?
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_author_tracks_list_context(request, author_id),
        'author_id': author_id,
        'author': author,
    }

    return render(
        request=request,
        template_name='tales_django/author_details.html.django',
        context=context,
    )


__all__ = ['author_details_view']
