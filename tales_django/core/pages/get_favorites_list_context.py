from django.contrib.auth.models import User
from django.http import HttpRequest

from core.logging import getDebugLogger
from tales_django.entities.Tracks.models import UserTrack
from tales_django.models import Track

favorites_limit = 20

logger = getDebugLogger()


def get_user_favorites(user: User):
    user_favorite_tracks = UserTrack.objects.filter(user=user, is_favorite=True).order_by('-favorited_at')
    user_favorite_track_ids = user_favorite_tracks.values_list('track_id', flat=True)
    favorites = Track.objects.filter(id__in=user_favorite_track_ids).filter(track_status='PUBLISHED')
    # NOTE: FUTURE: To use only UserTrack.is_favorite. Track.favorites is deprecated.
    favorites_old = user.favorite_tracks.filter(track_status='PUBLISHED').order_by('-published_at')
    favorites |= favorites_old
    favorites = favorites.distinct()
    # debugData = {
    #     'favorites': favorites,
    #     'favorites_old': favorites_old,
    #     'user_track': user_favorite_tracks,
    # }
    # logger.info(f'[get_user_favorites]: is_authenticated:\n{debugObj(debugData)}')
    return favorites


def get_favorites(request: HttpRequest):
    favorites = None
    if request.user.is_authenticated:
        favorites = get_user_favorites(request.user)
    else:
        favorites_cookie = request.COOKIES.get('favorites')
        if favorites_cookie is not None and favorites_cookie:
            # NOTE: This should be replaced by `UserTrack.is_favorite` field
            list_str = favorites_cookie.split('-')
            ids = list(filter(None, map(int, list_str)))
            # TODO: Ensure order by client list!
            favorites = (
                Track.objects.filter(pk__in=ids, track_status='PUBLISHED')
                # NOTE: Don't sort -- it should be sorted on the client, in this case
                # .order_by('-published_at', f'title_{language}')
                .all()
            )
            # Re-order favorites as it is on the client
            favorites = sorted(favorites, key=lambda it: ids.index(it.id))

    return favorites


def get_favorites_ids(request: HttpRequest):
    favorites = get_favorites(request)
    ids = map(lambda t: t.id, favorites)
    return ids


def get_favorites_list_context(request: HttpRequest):
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

    context = {
        'favorites': favorites_set,
        'favorites_count': favorites_count,
        'favorites_offset': favorites_offset,
        'favorites_limit': favorites_limit,
    }
    return context
