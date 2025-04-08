from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.models import Track

author_tracks_limit = 20

logger = getDebugLogger()


def get_author_tracks_list_context(request: HttpRequest, author_id: int):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tracks-list/big-tracks-list.django`):
    # - author_tracks
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - author_tracks_count
    # - author_tracks_offset
    # - author_tracks_limit
    # Regex:
    # \<\(author_tracks\|author_tracks_count\|author_tracks_offset\|author_tracks_limit\)\>

    author_tracks_offset = int(request.GET.get('author_tracks_offset', 0))

    # TODO: Use `author_id` in filter
    author_tracks = (
        Track.objects.filter(track_status='PUBLISHED', author_id=author_id)
        .order_by('-published_at', f'title_{language}')
        .all()
    )
    author_tracks_end = author_tracks_offset + author_tracks_limit
    author_tracks_set = author_tracks[author_tracks_offset:author_tracks_end]
    author_tracks_count = len(author_tracks)

    debugData = {
        'language': language,
        'author_tracks': author_tracks,
        'author_tracks_offset': author_tracks_offset,
    }
    debugStr = debugObj(debugData)
    logger.info(f'get_author_tracks_list_context\n{debugStr}')

    context = {
        # Tracks...
        'author_tracks': author_tracks_set,
        'author_tracks_count': author_tracks_count,
        'author_tracks_offset': author_tracks_offset,
        'author_tracks_limit': author_tracks_limit,
    }
    return context
