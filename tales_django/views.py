from .entities.App.views import RobotsView, components_demo, index_view, page403, page404, page500
from .entities.Users.views import UserRegistrationView, edit_user_profile, logout_user_route, profile

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
