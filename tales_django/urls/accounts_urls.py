# @module tales/urls/accounts.py
# @changed 2024.12.30, 00:13

from django.urls import include, path

from .. import views

# from ..forms import TalesRegistrationForm
# from ..views.user_registration import TalesRegistrationView

urlpatterns = [
    # # Accounts...
    # path(
    #     # Overrided registration form using updated one
    #     'accounts/register/',
    #     TalesRegistrationView.as_view(form_class=TalesRegistrationForm),
    #     name='django_registration_register',
    # ),
    path('profile', views.profile, name='profile'),
    # path(
    #     'profile/edit',
    #     views.edit_user_profile,
    #     name='profile_edit',
    # ),
    # Stock accounts...
    # path(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/successfully_logged_out/'}),
    path('logout/', views.logoutUser, name='logout_user'),
    path(
        'accounts/',
        include('django_registration.backends.activation.urls'),
    ),
    path('accounts/', include('django.contrib.auth.urls')),
]
