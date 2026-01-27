from django.utils.translation import gettext_lazy as _

from .entities.App.admin import SiteAdmin
from .entities.ContentBlocks.admin import ContentBlocksAdmin
from .entities.flatpages.admin import FlatPageAdmin
from .entities.Membership.admin import MembershipAdmin
from .entities.Tracks.admin import AuthorAdmin, RubricAdmin, SeriesAdmin, TagAdmin, TrackAdmin, UserTrackAdmin
from .entities.Users.admin import GroupAdmin, UserAdmin

__all__ = [
    'AuthorAdmin',
    'ContentBlocksAdmin',
    'FlatPageAdmin',
    'GroupAdmin',
    'MembershipAdmin',
    'RubricAdmin',
    'SeriesAdmin',
    'SiteAdmin',
    'TagAdmin',
    'TrackAdmin',
    'UserAdmin',
    'UserTrackAdmin',
]
