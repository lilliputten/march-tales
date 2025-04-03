from django.utils.translation import gettext_lazy as _

from .entities.Users.admin import UserAdmin, GroupAdmin
from .entities.App.admin import FlatPageAdmin
from .entities.Membership.admin import MembershipAdmin
from .entities.Tracks.admin import TrackAdmin, TagAdmin, RubricAdmin, AuthorAdmin


__all__ = [
    'UserAdmin',
    'GroupAdmin',
    'FlatPageAdmin',
    'MembershipAdmin',
    'TrackAdmin',
    'TagAdmin',
    'RubricAdmin',
    'AuthorAdmin',
]
