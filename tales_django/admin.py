from .entities.Users.admin import UserAdmin
from .entities.Membership.admin import MembershipAdmin
from .entities.Tracks.admin import TrackAdmin, TagAdmin, RubricAdmin, AuthorAdmin

__all__ = [
    'UserAdmin',
    'MembershipAdmin',
    'TrackAdmin',
    'TagAdmin',
    'RubricAdmin',
    'AuthorAdmin',
]
