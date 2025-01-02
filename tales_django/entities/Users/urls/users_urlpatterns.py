# @module tales_django/urls/accounts.py
# @changed 2024.12.30, 00:13

from django.urls import include, path

from ..forms import UserRegistrationForm
from ..views import (
    profile,
    UserRegistrationView,
    logout_user_route,
    edit_user_profile,
)

users_urlpatterns = [
    # Accounts...
    path(
        # Overrided registration form using updated one
        'accounts/register/',
        UserRegistrationView.as_view(form_class=UserRegistrationForm),
        name='django_registration_register',
    ),
    path('profile', profile, name='profile'),
    path(
        'profile/edit',
        edit_user_profile,
        name='profile_edit',
    ),
    # Stock accounts...
    # path(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/successfully_logged_out/'}),
    path('logout/', logout_user_route, name='logout_user'),
    path(
        'accounts/',
        include('django_registration.backends.activation.urls'),
    ),
    path('accounts/', include('django.contrib.auth.urls')),
]
