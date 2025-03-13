# from django.contrib.admin import AdminSite
# from django.utils.translation import gettext_lazy as _

from .entities.Users.admin import UserAdmin
from .entities.Membership.admin import MembershipAdmin
from .entities.Tracks.admin import TrackAdmin, TagAdmin, RubricAdmin, AuthorAdmin

# class AppAdminSite(AdminSite):
#     site_title = _('Hello World')
#     index_template = 'tales_django/dashboard.html'
#
#     def index(self, request, extra_context=None):
#         # Update extra_context with new variables
#         return super().index(request, extra_context)


__all__ = [
    'UserAdmin',
    'MembershipAdmin',
    'TrackAdmin',
    'TagAdmin',
    'RubricAdmin',
    'AuthorAdmin',
]
