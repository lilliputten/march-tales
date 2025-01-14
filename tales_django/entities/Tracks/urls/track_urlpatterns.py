from django.urls import path, include

from ..api import track_api_router

track_urlpatterns = [
    path(r'api/v1/', include(track_api_router.urls)),
]
