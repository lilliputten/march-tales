from django.http import HttpRequest

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

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tracks-list/big-tracks-list.django`):
    # - tracks
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - tracks_count
    # - tracks_offset
    # - tracks_limit

    order_args = get_track_order_args(request)
    filter_kwargs = get_track_filter_kwargs(request)
    filter_args = get_search_filter_args(request)

    tracks = Track.objects.filter(*filter_args, **filter_kwargs).distinct().order_by(*order_args)

    tracks_offset = int(request.GET.get('tracks_offset', 0))

    tracks_end = tracks_offset + tracks_limit
    tracks_set = tracks[tracks_offset:tracks_end]
    tracks_count = len(tracks)

    context = {
        'tracks': tracks_set,
        'tracks_count': tracks_count,
        'tracks_offset': tracks_offset,
        'tracks_limit': tracks_limit,
    }
    return context
