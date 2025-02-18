from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

# from django.utils.translation import gettext_lazy as _

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.pages import get_tracks_list_context
from tales_django.entities.Tracks.models import Track


logger = getDebugLogger()


def track_details_view(request: HttpRequest, track_id):

    track = get_object_or_404(Track, id=track_id)

    # TODO: Use get_generic_context (without tracks list)?
    context = {
        **get_tracks_list_context(request),
        'track_id': track_id,
        'track': track,
    }

    debugData = {
        'context': context,
    }
    debugStr = debugObj(debugData)
    logger.info(f'track_details_view\n{debugStr}')

    return render(
        request=request,
        template_name='tales_django/track_details.html.django',
        context=context,
    )


# __all__ = ['track_details_view']
