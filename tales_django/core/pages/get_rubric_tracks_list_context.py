from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.models import Track


rubric_tracks_limit = 20

logger = getDebugLogger()


def get_rubric_tracks_list_context(request: HttpRequest, rubric_id: int):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tracks-list/big-tracks-list.django`):
    # - rubric_tracks
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - rubric_tracks_count
    # - rubric_tracks_offset
    # - rubric_tracks_limit
    # Regex:
    # \<\(rubric_tracks\|rubric_tracks_count\|rubric_tracks_offset\|rubric_tracks_limit\)\>

    rubric_tracks_offset = int(request.GET.get('rubric_tracks_offset', 0))

    # TODO: Use `rubric_id` in filter
    rubric_tracks = (
        Track.objects.filter(track_status='PUBLISHED', rubrics__id=rubric_id)
        .order_by('-published_at', f'title_{language}')
        .all()
    )
    rubric_tracks_end = rubric_tracks_offset + rubric_tracks_limit
    rubric_tracks_set = rubric_tracks[rubric_tracks_offset:rubric_tracks_end]
    rubric_tracks_count = len(rubric_tracks)

    debugData = {
        'language': language,
        'rubric_tracks': rubric_tracks,
        'rubric_tracks_offset': rubric_tracks_offset,
    }
    debugStr = debugObj(debugData)
    logger.info(f'get_rubric_tracks_list_context\n{debugStr}')

    context = {
        # Tracks...
        'rubric_tracks': rubric_tracks_set,
        'rubric_tracks_count': rubric_tracks_count,
        'rubric_tracks_offset': rubric_tracks_offset,
        'rubric_tracks_limit': rubric_tracks_limit,
    }
    return context
