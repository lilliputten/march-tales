from django.urls import path

from .tick_api_view import tick_api_view
from .check_api_view import check_api_view
from .logout_api_view import logout_api_view
from .favorites_ids_api_view import favorites_ids_api_view


api_urlpatterns = [
    # API
    # path(r'api/v1/', include(test_api_router.urls)),
    path('api/v1/tick/', tick_api_view),
    path('api/v1/check/', check_api_view),
    path('api/v1/favorites/ids/', favorites_ids_api_view),
    path('api/v1/logout/', logout_api_view),
]

__all__ = [
    'api_urlpatterns',
]
