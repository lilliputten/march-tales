from django.http import HttpRequest
from django.utils import translation
from django.db.models import Count

from core.logging import getDebugLogger

from tales_django.models import Rubric
from tales_django.models import Tag
from tales_django.models import Author


show_authors_count = 20
show_favorite_tracks_count = 20

logger = getDebugLogger()


def get_common_context(request: HttpRequest):
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

    # # Favorite tracks...
    # # NOTE: Implemented in the dedicated context
    # # @see `tales_django/core/pages/get_favorites_list_context.py`
    # favorite_tracks = None
    # if request.user.is_authenticated:
    #     favorite_tracks = (
    #         request.user.favorite_tracks
    #         # .filter(track_status='PUBLISHED')
    #         .order_by('-published_at').all()
    #     )
    # else:
    #     favorites_cookie = request.COOKIES.get('favorites')
    #     if favorites_cookie is not None and favorites_cookie:
    #         list_str = favorites_cookie.split(',')
    #         list = filter(None, map(int, list_str))

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
        # # Favorite tracks...
        # # NOTE: Implemented in the dedicated context
        # # @see `tales_django/core/pages/get_favorites_list_context.py`
        # 'favorite_tracks': favorite_tracks[:show_favorite_tracks_count] if favorite_tracks else None,
        # 'has_more_favorite_tracks': len(favorite_tracks) > show_favorite_tracks_count if favorite_tracks else None,
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
