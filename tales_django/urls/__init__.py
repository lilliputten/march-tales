from .accounts_urls import urlpatterns as accounts_urlpatterns
from .root_urls import urlpatterns as root_urlpatterns

from ..entities.Membership.urls import membership_urlpatterns

urlpatterns = accounts_urlpatterns + membership_urlpatterns + root_urlpatterns
