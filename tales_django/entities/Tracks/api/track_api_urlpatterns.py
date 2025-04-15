from django.urls import path

from .sync_user_tracks_api_view import sync_user_tracks_api_view

track_api_urlpatterns = [
    # API
    path('api/v1/user/tracks/sync/', sync_user_tracks_api_view),
]

__all__ = [
    'track_api_urlpatterns',
]
