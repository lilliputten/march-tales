from .entities.App.urls import root_urlpatterns
from .entities.Users.urls import users_urlpatterns
from .entities.Membership.urls import membership_urlpatterns

urlpatterns = users_urlpatterns + membership_urlpatterns + root_urlpatterns
