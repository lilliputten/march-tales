from django.urls import path, include

from .views import track_details_view
from .api import track_api_router

track_urlpatterns = [
    path(r'tracks/<int:track_id>/', track_details_view, name='track_details'),
    path(r'api/v1/', include(track_api_router.urls)),
]
