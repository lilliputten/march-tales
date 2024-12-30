# # @module tales/urls/__init__.py
# # @changed 2024.04.02, 00:32

from .accounts_urls import urlpatterns as accounts_urlpatterns

# from .event_urls import urlpatterns as event_urlpatterns
# from .membership_urls import urlpatterns as membership_urlpatterns
# from .payments_urls import urlpatterns as payment_urlpatterns
from .root_urls import urlpatterns as root_urlpatterns

urlpatterns = accounts_urlpatterns + root_urlpatterns

# + event_urlpatterns \
# + payment_urlpatterns \
# + membership_urlpatterns
