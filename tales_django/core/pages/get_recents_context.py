import random

from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.entities.Tracks.api.track_serializers import TrackSerializer
from tales_django.entities.Tracks.models import Author, Rubric, Tag
from tales_django.models import Track

logger = getDebugLogger()


def get_recents_context(request: HttpRequest, serialize: bool = False):

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

    random_track: Track
    # Ensure that random track isn't the same as the `most_recent_track`
    counter = 0
    while counter < 5:
        random_idx = random.randrange(0, total_tracks_count)
        random_track = recent_tracks[random_idx] if total_tracks_count else None
        if random_track != most_recent_track:
            break
        counter += 1

    authors = Author.objects.all()
    rubrics = Rubric.objects.all()
    tags = Tag.objects.all()

    context = {
        'stats': {
            'tracks_count': total_tracks_count,
            'authors_count': len(authors),
            'rubrics_count': len(rubrics),
            'tags_count': len(tags),
        },
        'recent_tracks': recent_tracks_set,
        'popular_tracks': popular_tracks_set,
        'most_recent_track': most_recent_track,
        'random_track': random_track,
    }

    if serialize:
        serializer_context = {'request': request}
        # Serialize context data using TrackSerializer
        context['recent_tracks'] = TrackSerializer(recent_tracks_set, many=True, context=serializer_context).data
        context['popular_tracks'] = TrackSerializer(popular_tracks_set, many=True, context=serializer_context).data
        context['most_recent_track'] = (
            TrackSerializer(most_recent_track, context=serializer_context).data if most_recent_track else None
        )
        context['random_track'] = (
            TrackSerializer(random_track, context=serializer_context).data if random_track else None
        )

    # debugStr = debugObj(context)
    # logger.info(f'get_recents_context\n{debugStr}')

    return context
