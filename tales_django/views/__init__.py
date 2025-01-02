# @module tales_django/views/__init__.py
# @changed 2024.03.15, 19:53

from .root_views import (
    components_demo,
    index,
)
from .system_views import (
    RobotsView,
    page403,
    page404,
    page500,
)
from ..entities.Users.views import (
    profile,
    logout_user_route,
    edit_user_profile,
    UserRegistrationView,
)

__all__ = [
    'components_demo',
    'index',
    'profile',
    'logout_user_route',
    'RobotsView',
    'page403',
    'page404',
    'page500',
    'UserRegistrationView',
    'edit_user_profile',
]
