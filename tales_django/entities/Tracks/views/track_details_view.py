from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from core.logging import getDebugLogger
from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import get_common_context, get_favorites_list_context, get_tracks_list_context
from tales_django.entities.Tracks.models import Track, UserTrack

logger = getDebugLogger()


@check_locale_decorator
def track_details_view(request: HttpRequest, track_id):

    track = get_object_or_404(Track, id=track_id)

    context = {
        **get_common_context(request),
        **get_tracks_list_context(request),
        **get_favorites_list_context(request),
        # 'track_id': track_id,
        'track': track,
    }

    if request.user.is_authenticated:
        user_track = UserTrack.objects.get(user=request.user, track=track)
        context['user_track'] = user_track

    response = render(
        request=request,
        template_name='tales_django/track_details.html.django',
        context=context,
    )

    return response


__all__ = ['track_details_view']
