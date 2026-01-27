from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from .views import rubric_details_view, rubric_index_view

# Content routes with language prefix support
rubric_urlpatterns = i18n_patterns(
    path(r'rubrics/', rubric_index_view, name='rubric_index'),
    path(r'rubrics/<int:rubric_id>/', rubric_details_view, name='rubric_details'),
)
