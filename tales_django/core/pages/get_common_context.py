from django.db.models import Count
from django.http import HttpRequest
from django.utils import translation

from core.logging import getDebugLogger
from tales_django.models import Author, Rubric, Tag

show_authors_count = 20
show_favorite_tracks_count = 20

logger = getDebugLogger()


def get_common_context(request: HttpRequest):
    language = translation.get_language()

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
    }
    return context
