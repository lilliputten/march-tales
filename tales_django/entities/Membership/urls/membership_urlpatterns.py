from django.urls import path

from ..views import membership_application

membership_urlpatterns = [
    path(
        'membership/apply',
        membership_application,
        name='membership_application',
    ),
]
