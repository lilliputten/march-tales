from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from core.logging import getDebugLogger
from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import get_common_context, get_favorites_list_context, get_rubric_tracks_list_context
from tales_django.entities.Tracks.models import Rubric

logger = getDebugLogger()


@check_locale_decorator
def rubric_details_view(request: HttpRequest, rubric_id):
    rubric = get_object_or_404(Rubric, id=rubric_id)

    # TODO: Use get_generic_context (without rubrics list)?
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_rubric_tracks_list_context(request, rubric_id),
        'rubric_id': rubric_id,
        'rubric': rubric,
    }

    return render(
        request=request,
        template_name='tales_django/rubric_details.html.django',
        context=context,
    )


__all__ = ['rubric_details_view']
