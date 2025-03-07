from rest_framework import routers

from .AuthorViewSet import AuthorViewSet

from .TrackViewSet import TrackViewSet

# Routers provide an easy way of automatically determining the URL conf.
# @see https://www.django-rest-framework.org/api-guide/routers/
track_api_router = routers.DefaultRouter()
track_api_router.register(r'tracks', TrackViewSet)
track_api_router.register(r'authors', AuthorViewSet)

__all__ = [
    'track_api_router',
]
