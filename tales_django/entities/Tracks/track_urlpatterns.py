from django.urls import include, path

from .api import track_api_router
from .views import favorites_view, track_details_view

track_urlpatterns = [
    path(r'tracks/<int:track_id>/', track_details_view, name='track_details'),
    path(r'favorites/', favorites_view, name='favorites'),
    path(r'favorites/<int:track_id>/', track_details_view, name='favorite_details'),
    path(r'api/v1/', include(track_api_router.urls)),
]
