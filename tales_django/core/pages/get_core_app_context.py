from django.http import HttpRequest
from django.utils import translation
from django.db.models import Count

from core.logging import getDebugLogger

from tales_django.models import Track
from tales_django.models import Rubric
from tales_django.models import Tag
from tales_django.models import Author

showAuthorsCount = 3
showTracksCount = 3
showFavoriteTracksCount = showTracksCount

logger = getDebugLogger()


def get_core_app_context(request: HttpRequest):
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
    logger.info(f'language: {language}')

    favorite_tracks = None
    if request.user.is_authenticated:
        favorite_tracks = (
            request.user.favorite_tracks
            # .filter(track_status='PUBLISHED')
            .order_by('-published_at').all()
        )

    # TODO: Add popular tracks (show instead of recent ones?)

    tracks = Track.objects.filter(track_status='PUBLISHED').order_by('-published_at', f'title_{language}').all()

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
        'user': request.user,
        'tracks': tracks[:showTracksCount],
        'favorite_tracks': favorite_tracks[:showFavoriteTracksCount] if favorite_tracks else None,
        'has_more_favorite_tracks': len(favorite_tracks) > showFavoriteTracksCount if favorite_tracks else None,
        'has_more_tracks': len(tracks) > showTracksCount,
        'authors': authors[:showAuthorsCount],
        'has_more_authors': len(authors) > showAuthorsCount,
        'rubrics': rubrics,
        'tags': tags,
        # # Translation examples...
        # 'sample_text': _('Sample Message'),
        # 'plural_test': plural_test,
    }
    return context
