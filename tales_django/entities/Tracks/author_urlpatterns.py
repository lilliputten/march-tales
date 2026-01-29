from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from .views.author_details_view import author_details_view
from .views.author_index_view import author_index_view

# Content routes with language prefix support
author_urlpatterns = i18n_patterns(
    path(r'authors/', author_index_view, name='author_index'),
    path(r'authors/<int:author_id>/', author_details_view, name='author_details'),
)
