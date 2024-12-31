from .accounts_urls import urlpatterns as accounts_urlpatterns
from .membership_urls import urlpatterns as membership_urlpatterns
from .root_urls import urlpatterns as root_urlpatterns

urlpatterns = accounts_urlpatterns + membership_urlpatterns + root_urlpatterns
