import math

from django.http import HttpRequest
from django.utils import translation
from django.db.models import Count

from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.models import Track
from tales_django.models import Rubric
from tales_django.models import Tag
from tales_django.models import Author

from .get_common_context import get_common_context


tracks_limit = 10
# tracks_offset = 0

show_authors_count = 3
show_favorite_tracks_count = tracks_limit

logger = getDebugLogger()


def get_tracks_list_context(request: HttpRequest):

    common_context = get_common_context(request)

    language = translation.get_language()

    # Tracks...

    # Expected params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tracks-list/big-tracks-list.django`):
    # - tracks
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - tracks_count
    # - tracks_offset
    # - tracks_limit
    # Regex:
    # \<\(tracks\|tracks_count\|tracks_offset\|tracks_limit\)\>

    tracks_offset = int(request.GET.get('tracks_offset', 0))
    tracks = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}').all()
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
        **common_context,
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
