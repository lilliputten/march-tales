from rest_framework import routers

from .TrackViewSet import TrackViewSet

# Routers provide an easy way of automatically determining the URL conf.
track_api_router = routers.DefaultRouter()
track_api_router.register(r'api-tracks', TrackViewSet)

__all__ = [
    'track_api_router',
]
