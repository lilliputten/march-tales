from django.http import HttpRequest
from django.utils import translation

from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.models import Track


favorites_limit = 20

logger = getDebugLogger()


def get_favorites(request: HttpRequest):

    language = translation.get_language()

    favorites = None
    if request.user.is_authenticated:
        favorites = request.user.favorite_tracks.filter(track_status='PUBLISHED').order_by('-published_at').all()
    else:
        favorites_cookie = request.COOKIES.get('favorites')
        if favorites_cookie is not None and favorites_cookie:
            list_str = favorites_cookie.split('-')
            ids = filter(None, map(int, list_str))
            favorites = (
                Track.objects.filter(pk__in=ids, track_status='PUBLISHED')
                .order_by('-published_at', f'title_{language}')
                .all()
            )

    return favorites


def get_favorites_ids(request: HttpRequest):

    if request.user.is_authenticated:
        favorites = request.user.favorite_tracks.filter(track_status='PUBLISHED').order_by('-published_at').all()
        ids = map(lambda t: t.id, favorites)
        return ids
    else:
        favorites_cookie = request.COOKIES.get('favorites')
        if favorites_cookie is not None and favorites_cookie:
            list_str = favorites_cookie.split('-')
            ids = filter(None, map(int, list_str))
            return ids


def get_favorites_list_context(request: HttpRequest):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-favorites-list/big-favorites-list.django`):
    # - favorites
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - favorites_count
    # - favorites_offset
    # - favorites_limit
    # Regex:
    # \<\(favorites\|favorites_count\|favorites_offset\|favorites_limit\)\>

    favorites = get_favorites(request)

    favorites_offset = int(request.GET.get('favorites_offset', 0))

    favorites_end = favorites_offset + favorites_limit
    favorites_set = favorites[favorites_offset:favorites_end] if favorites is not None and favorites else None
    favorites_count = len(favorites) if favorites is not None and favorites else 0

    debugData = {
        'language': language,
        'favorites_offset': favorites_offset,
    }
    debugStr = debugObj(debugData)
    logger.info(f'get_favorites_list_context\n{debugStr}')

    context = {
        'favorites': favorites_set,
        'favorites_count': favorites_count,
        'favorites_offset': favorites_offset,
        'favorites_limit': favorites_limit,
    }
    return context
