from rest_framework import routers

from .TrackViewSet import TrackViewSet

# Routers provide an easy way of automatically determining the URL conf.
# @see https://www.django-rest-framework.org/api-guide/routers/
track_api_router = routers.DefaultRouter()
track_api_router.register(r'tracks', TrackViewSet)

__all__ = [
    'track_api_router',
]
