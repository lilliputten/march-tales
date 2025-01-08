from .entities.App.views import (
    components_demo,
    index_view,
    RobotsView,
    page403,
    page404,
    page500,
)
from .entities.Users.views import (
    profile,
    logout_user_route,
    edit_user_profile,
    UserRegistrationView,
)

__all__ = [
    'components_demo',
    'index_view',
    'profile',
    'logout_user_route',
    'RobotsView',
    'page403',
    'page404',
    'page500',
    'UserRegistrationView',
    'edit_user_profile',
]
