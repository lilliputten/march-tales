from .entities.Users.models import User
from .entities.Membership.models import Membership
from .entities.Tracks.models import Track, Tag, Rubric, Author

__all__ = [
    'User',
    'Membership',
    'Track',
    'Tag',
    'Rubric',
    'Author',
]

# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
#
# content_type = ContentType.objects.get_for_model(Track)
# permission = Permission.objects.create(
#     codename='import_track',
#     name=_('Can import track'),
#     content_type=content_type,
# )
#
