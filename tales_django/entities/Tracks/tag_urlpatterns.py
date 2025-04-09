from django.urls import path

from .views import tag_details_view, tag_index_view

tag_urlpatterns = [
    path(r'tags/', tag_index_view, name='tag_index'),
    path(r'tags/<int:tag_id>/', tag_details_view, name='tag_details'),
]
