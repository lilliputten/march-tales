# @module tales/views/__init__.py
# @changed 2024.03.15, 19:53

from .root_views import (
    components_demo,
    index,
    profile,
)
from .accounts_views import (
    logoutUser,
)
from .system_views import (
    RobotsView,
    page403,
    page404,
    page500,
)

# from .user import edit_user_profile  # SignUpView,
# from .user_registration import DdsRegistrationView

__all__ = [
    'components_demo',
    'index',
    'profile',
    'logoutUser',
    'RobotsView',
    'page403',
    'page404',
    'page500',
]
