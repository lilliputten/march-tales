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


tracks_limit = 10
# tracks_offset = 0

show_authors_count = 3
show_favorite_tracks_count = tracks_limit

logger = getDebugLogger()


def get_common_context(request: HttpRequest):
    # # TODO: Get favrites/playlist for the user (if logged in)
    # events = [obj for obj in Event.objects.filter(public=True) if obj.can_register]
    # if request.user.is_authenticated:
    #     for event in events:
    #         event.registration = event.get_active_event_registration_for_user(request.user)

    # # Translation examples...
    # count = 21
    # plural_test = ngettext_lazy('there is %(count)d object', 'there are %(count)d objects', count,) % {
    #     'count': count,
    # }

    language = translation.get_language()

    # Favorite tracks...
    favorite_tracks = None
    if request.user.is_authenticated:
        favorite_tracks = (
            request.user.favorite_tracks
            # .filter(track_status='PUBLISHED')
            .order_by('-published_at').all()
        )

    # TODO: Add popular tracks (show instead of recent ones?)

    # # Tracks...
    # tracks_offset = int(request.GET.get('tracks_offset', 0))
    # tracks = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}').all()
    # tracks_end = tracks_offset + tracks_limit
    # tracks_set = tracks[tracks_offset:tracks_end]
    # tracks_count = len(tracks)
    # has_prev_tracks = tracks_offset > 0
    # has_next_tracks = tracks_count > tracks_end
    # tracks_page_no = math.floor(tracks_offset / tracks_limit) + 1
    # tracks_pages_count = math.ceil(tracks_count / tracks_limit)
    #
    # debugData = {
    #     'language': language,
    #     'tracks_offset': tracks_offset,
    # }
    # debugStr = debugObj(debugData)
    # logger.info(f'get_common_context\n{debugStr}')

    # Authors...
    authors = (
        Author.objects.annotate(t_count=Count('track', distinct=True)).order_by('-t_count', f'name_{language}').all()
    )
    rubrics = (
        Rubric.objects.annotate(t_count=Count('tracks'))
        .filter(t_count__gt=0)
        .order_by('-t_count', f'text_{language}')
        .all()
    )
    tags = (
        Tag.objects.annotate(t_count=Count('tracks'))
        .filter(t_count__gt=0)
        .order_by('-t_count', f'text_{language}')
        .all()
    )
    context = {
        # User...
        'user': request.user,
        # # Tracks...
        # 'tracks': tracks_set,
        # 'tracks_count': tracks_count,
        # 'tracks_offset': tracks_offset,
        # 'tracks_limit': tracks_limit,
        # 'has_prev_tracks': has_prev_tracks,
        # 'has_next_tracks': has_next_tracks,
        # 'tracks_page_no': tracks_page_no,
        # 'tracks_pages_count': tracks_pages_count,
        # Favorite tracks...
        'favorite_tracks': favorite_tracks[:show_favorite_tracks_count] if favorite_tracks else None,
        'has_more_favorite_tracks': len(favorite_tracks) > show_favorite_tracks_count if favorite_tracks else None,
        # Authors...
        'authors': authors[:show_authors_count],
        'has_more_authors': len(authors) > show_authors_count,
        # Other...
        'rubrics': rubrics,
        'tags': tags,
        # # Translation examples...
        # 'sample_text': _('Sample Message'),
        # 'plural_test': plural_test,
    }
    return context
