# @module tales_django/urls/accounts.py
# @changed 2024.12.30, 00:13

from django.urls import include, path

from ..forms import UserRegistrationForm
from ..views import (
    UserRegistrationView,
    delete_user_account,
    edit_user_profile,
    login_success,
    logout_user_route,
    profile,
)

users_urlpatterns = [
    # Accounts...
    path(
        # Overrided registration form using updated one
        r'accounts/register/',
        UserRegistrationView.as_view(form_class=UserRegistrationForm),
        name='django_registration_register',
    ),
    path(r'login-success/', login_success, name='login_success'),
    path(r'login-success/<str:key>/', login_success, name='login_success'),
    path(r'profile/', profile, name='profile'),
    path(r'profile/edit', edit_user_profile, name='profile_edit'),
    path(r'profile/delete', delete_user_account, name='delete_account'),
    # Stock accounts...
    # path(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/successfully_logged_out/'}),
    path(r'logout/', logout_user_route, name='logout_user'),
    path(
        r'accounts/',
        include('django_registration.backends.activation.urls'),
    ),
    # allauth, @see https://docs.allauth.org/en/latest/installation/quickstart.html
    path('accounts/', include('allauth.urls')),
    path('_allauth/', include('allauth.headless.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
