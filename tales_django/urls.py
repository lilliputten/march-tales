from .entities.App.app_urlpatterns import app_urlpatterns, handler404, handler403, handler500

from .entities.Users.urls import users_urlpatterns
from .entities.Membership.urls import membership_urlpatterns
from .entities.Tracks.urls import track_urlpatterns

urlpatterns = users_urlpatterns + membership_urlpatterns + app_urlpatterns + track_urlpatterns

__all__ = [
    'handler404',
    'handler403',
    'handler500',
]
