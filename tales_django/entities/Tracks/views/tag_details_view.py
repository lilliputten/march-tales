from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from core.logging import getDebugLogger
from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import (get_common_context,
                                     get_favorites_list_context,
                                     get_tag_tracks_list_context)
from tales_django.entities.Tracks.models import Tag

logger = getDebugLogger()


@check_locale_decorator
def tag_details_view(request: HttpRequest, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    # TODO: Use get_generic_context (without tags list)?
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tag_tracks_list_context(request, tag_id),
        'tag_id': tag_id,
        'tag': tag,
    }

    return render(
        request=request,
        template_name='tales_django/tag_details.html.django',
        context=context,
    )


__all__ = ['tag_details_view']
