# from rest_framework import routers
from django.urls import path

# from .TestViewSet import TestViewSet
from .TickViewSet import TickApiView
from .CheckViewSet import CheckApiView

# Routers provide an easy way of automatically determining the URL conf.
# api_router = routers.DefaultRouter()
# api_router.register(r'test-view', TestViewSet, basename='test')

api_urlpatterns = [
    # API
    # path(r'api/v1/', include(test_api_router.urls)),
    path('api/v1/tick/', TickApiView.as_view()),
    path('api/v1/check/', CheckApiView.as_view()),
]

__all__ = [
    'api_urlpatterns',
]
