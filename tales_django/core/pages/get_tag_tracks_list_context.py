from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.models import Track


tag_tracks_limit= 20

logger = getDebugLogger()


def get_tag_tracks_list_context(request: HttpRequest, tag_id: int):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tracks-list/big-tracks-list.django`):
    # - tag_tracks
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - tag_tracks_count
    # - tag_tracks_offset
    # - tag_tracks_limit
    # Regex:
    # \<\(tag_tracks\|tag_tracks_count\|tag_tracks_offset\|tag_tracks_limit\)\>

    tag_tracks_offset = int(request.GET.get('tag_tracks_offset', 0))

    # TODO: Use `tag_id` in filter
    tag_tracks = (
        Track.objects.filter(track_status='PUBLISHED', tags__id=tag_id)
        .order_by('-published_at', f'title_{language}')
        .all()
    )
    tag_tracks_end = tag_tracks_offset + tag_tracks_limit
    tag_tracks_set = tag_tracks[tag_tracks_offset:tag_tracks_end]
    tag_tracks_count = len(tag_tracks)

    debugData = {
        'language': language,
        'tag_tracks': tag_tracks,
        'tag_tracks_offset': tag_tracks_offset,
    }
    debugStr = debugObj(debugData)
    logger.info(f'get_tag_tracks_list_context\n{debugStr}')

    context = {
        # Tracks...
        'tag_tracks': tag_tracks_set,
        'tag_tracks_count': tag_tracks_count,
        'tag_tracks_offset': tag_tracks_offset,
        'tag_tracks_limit': tag_tracks_limit,
    }
    return context
