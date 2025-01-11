from .entities.App.urls import root_urlpatterns, handler404, handler403, handler500
from .entities.Users.urls import users_urlpatterns
from .entities.Membership.urls import membership_urlpatterns

urlpatterns = users_urlpatterns + membership_urlpatterns + root_urlpatterns

__all__ = [
    'handler404',
    'handler403',
    'handler500',
]
