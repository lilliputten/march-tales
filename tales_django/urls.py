from tales_django.entities.Tracks.api import track_api_urlpatterns

from .entities.App.app_urlpatterns import app_urlpatterns, handler403, handler404, handler500
from .entities.Membership.urls import membership_urlpatterns
from .entities.Tracks.author_urlpatterns import author_urlpatterns
from .entities.Tracks.rubric_urlpatterns import rubric_urlpatterns
from .entities.Tracks.tag_urlpatterns import tag_urlpatterns
from .entities.Tracks.track_urlpatterns import track_urlpatterns
from .entities.Users.urls import users_urlpatterns

urlpatterns = (
    users_urlpatterns
    + membership_urlpatterns
    + app_urlpatterns
    + track_urlpatterns
    + track_api_urlpatterns
    + author_urlpatterns
    + rubric_urlpatterns
    + tag_urlpatterns
)

__all__ = [
    'handler404',
    'handler403',
    'handler500',
]
