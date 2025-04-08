from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.entities.Tracks.api.track_filters import (
    get_search_filter_args,
    get_track_filter_kwargs,
    get_track_order_args,
)
from tales_django.models import Track

tracks_limit = 20

logger = getDebugLogger()


def get_tracks_list_context(request: HttpRequest):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tracks-list/big-tracks-list.django`):
    # - tracks
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - tracks_count
    # - tracks_offset
    # - tracks_limit
    # Regex:
    # \<\(tracks\|tracks_count\|tracks_offset\|tracks_limit\)\>

    order_args = get_track_order_args(request)
    filter_kwargs = get_track_filter_kwargs(request)
    filter_args = get_search_filter_args(request)

    tracks = Track.objects.filter(*filter_args, **filter_kwargs).distinct().order_by(*order_args)
    # tracks = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}').all()

    tracks_offset = int(request.GET.get('tracks_offset', 0))

    tracks_end = tracks_offset + tracks_limit
    tracks_set = tracks[tracks_offset:tracks_end]
    tracks_count = len(tracks)
    # has_prev_tracks = tracks_offset > 0
    # has_next_tracks = tracks_count > tracks_end
    # tracks_page_no = math.floor(tracks_offset / tracks_limit) + 1
    # tracks_pages_count = math.ceil(tracks_count / tracks_limit)

    debugData = {
        'language': language,
        'tracks_offset': tracks_offset,
    }
    debugStr = debugObj(debugData)
    logger.info(f'get_tracks_list_context\n{debugStr}')

    context = {
        # Tracks...
        'tracks': tracks_set,
        'tracks_count': tracks_count,
        'tracks_offset': tracks_offset,
        'tracks_limit': tracks_limit,
        # 'has_prev_tracks': has_prev_tracks,
        # 'has_next_tracks': has_next_tracks,
        # 'tracks_page_no': tracks_page_no,
        # 'tracks_pages_count': tracks_pages_count,
    }
    return context
