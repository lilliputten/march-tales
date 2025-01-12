from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# from django.utils.translation import ngettext_lazy

from tales_django.models import Track
from tales_django.models import Rubric
from tales_django.models import Tag
from tales_django.models import Author


def index_view(request: HttpRequest):
    # # TODO: Get favrites/playlist for the user (if logged in)
    # events = [obj for obj in Event.objects.filter(public=True) if obj.can_register]
    # if request.user:
    #     for event in events:
    #         event.registration = event.get_active_event_registration_for_user(request.user)

    # # Translation examples...
    # count = 21
    # plural_test = ngettext_lazy('there is %(count)d object', 'there are %(count)d objects', count,) % {
    #     'count': count,
    # }
    favorite_tracks = request.user.favorite_tracks if not request.user.is_anonymous else None
    tracks = Track.objects.all()
    rubrics = Rubric.objects.all()
    tags = Tag.objects.all()
    authors = Author.objects.all()
    return render(
        request=request,
        template_name='tales_django/index.html.django',
        context={
            'user': request.user,
            'favorite_tracks': favorite_tracks,
            'tracks': tracks,
            'rubrics': rubrics,
            'tags': tags,
            'authors': authors,
            # # Translation examples...
            # 'sample_text': _('Sample Message'),
            # 'plural_test': plural_test,
        },
    )


__all__ = ['index_view']
