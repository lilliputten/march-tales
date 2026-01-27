from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from ..views import membership_application

# Content routes with language prefix support
membership_urlpatterns = i18n_patterns(
    path(
        'membership/apply',
        membership_application,
        name='membership_application',
    ),
)
