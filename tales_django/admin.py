from django.utils.translation import gettext_lazy as _

from .entities.App.admin import FlatPageAdmin
from .entities.Users.admin import UserAdmin, GroupAdmin
from .entities.Membership.admin import MembershipAdmin
from .entities.Tracks.admin import TrackAdmin, TagAdmin, RubricAdmin, AuthorAdmin


__all__ = [
    'FlatPageAdmin',
    'UserAdmin',
    'GroupAdmin',
    'MembershipAdmin',
    'TrackAdmin',
    'TagAdmin',
    'RubricAdmin',
    'AuthorAdmin',
]
