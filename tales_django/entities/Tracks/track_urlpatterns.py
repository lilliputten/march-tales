from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from .api import track_api_router
from .views import favorites_view, track_details_view

# Content routes with language prefix support
track_urlpatterns = i18n_patterns(
    path(r'tracks/<int:track_id>/', track_details_view, name='track_details'),
    path(r'favorites/', favorites_view, name='favorites'),
    path(r'favorites/<int:track_id>/', track_details_view, name='favorite_details'),
)

# API routes - no language prefix (standard practice)
track_api_urlpatterns = [
    path(r'api/v1/', include(track_api_router.urls)),
]
