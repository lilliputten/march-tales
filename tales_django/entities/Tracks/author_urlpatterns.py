from django.urls import path

from .views import author_details_view, author_index_view

author_urlpatterns = [
    path(r'authors/', author_index_view, name='author_index'),
    path(r'authors/<int:author_id>/', author_details_view, name='author_details'),
]
