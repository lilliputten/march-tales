from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from .views import tag_details_view, tag_index_view

# Content routes with language prefix support
tag_urlpatterns = i18n_patterns(
    path(r'tags/', tag_index_view, name='tag_index'),
    path(r'tags/<int:tag_id>/', tag_details_view, name='tag_details'),
)
