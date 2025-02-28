# from rest_framework import routers
from django.urls import path

from .tick_api_view import tick_api_view
from .check_api_view import check_api_view
from .logout_api_view import logout_api_view

# Routers provide an easy way of automatically determining the URL conf.
# api_router = routers.DefaultRouter()
# api_router.register(r'test-view', TestViewSet, basename='test')

api_urlpatterns = [
    # API
    # path(r'api/v1/', include(test_api_router.urls)),
    path('api/v1/tick/', tick_api_view),
    path('api/v1/check/', check_api_view),
    path('api/v1/logout/', logout_api_view),
]

__all__ = [
    'api_urlpatterns',
]
