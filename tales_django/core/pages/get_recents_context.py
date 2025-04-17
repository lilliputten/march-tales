import random

from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.models import Track

logger = getDebugLogger()


def get_recents_context(request: HttpRequest):

    language = translation.get_language()

    recent_tracks = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}').all()
    popular_tracks = (
        Track.objects.filter(track_status='PUBLISHED')
        .order_by('-played_count', '-published_at', f'title_{language}')
        .all()
    )

    # Show only 3 recent/popular tracks
    recent_tracks_set = recent_tracks[:3]
    popular_tracks_set = popular_tracks[:3]

    total_tracks_count = len(recent_tracks)

    most_recent_track = recent_tracks[0] if total_tracks_count else None

    random_idx = random.randrange(0, total_tracks_count)
    random_track = recent_tracks[random_idx] if total_tracks_count else None
    # TODO: Ensure that random track isn't the same as the `most_recent_track`

    debugData = {
        'recent_tracks': recent_tracks_set,
        'popular_tracks': popular_tracks_set,
        'most_recent_track': most_recent_track,
        'random_track': random_track,
    }
    debugStr = debugObj(debugData)
    logger.info(f'get_recents_context\n{debugStr}')

    context = {
        'recent_tracks': recent_tracks_set,
        'popular_tracks': popular_tracks_set,
        'most_recent_track': most_recent_track,
        'random_track': random_track,
    }
    return context
