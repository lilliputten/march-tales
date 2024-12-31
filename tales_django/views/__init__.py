# @module tales_django/views/__init__.py
# @changed 2024.03.15, 19:53

from .root_views import (
    components_demo,
    index,
    profile,
)
from .accounts_views import (
    logoutUserRoute,
)
from .system_views import (
    RobotsView,
    page403,
    page404,
    page500,
)
from .edit_user_profile import edit_user_profile

from .UserRegistrationView import UserRegistrationView

__all__ = [
    'components_demo',
    'index',
    'profile',
    'logoutUserRoute',
    'RobotsView',
    'page403',
    'page404',
    'page500',
    'UserRegistrationView',
    'edit_user_profile',
]
