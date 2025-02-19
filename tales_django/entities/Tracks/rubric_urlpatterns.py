from django.urls import path

from .views import rubric_index_view, rubric_details_view

rubric_urlpatterns = [
    path(r'rubrics/', rubric_index_view, name='rubric_index'),
    path(r'rubrics/<int:rubric_id>/', rubric_details_view, name='rubric_details'),
]
