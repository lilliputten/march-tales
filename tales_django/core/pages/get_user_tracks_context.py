from django.http import HttpRequest

from tales_django.entities.Tracks.models import UserTrack


def get_user_tracks_context(request: HttpRequest):

    user_tracks = UserTrack.objects.filter(user=request.user).all() if request.user.is_authenticated else None

    context = {
        'user_tracks': user_tracks,
    }
    return context
