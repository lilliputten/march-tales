from django.db import models
from django.db.models import Model

from core.helpers.dates import this_year

from .MembershipData import MembershipData


MEMBERSHIP_DATA = MembershipData()


class Membership(Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    membership_type = models.TextField(choices=MEMBERSHIP_DATA.choices, default=MEMBERSHIP_DATA.default)

    started = models.IntegerField(default=this_year)
    until = models.IntegerField(default=this_year)

    # TODO: Implement payment methods
    # payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True)

    mailing_list = models.BooleanField(default=False)

    @property
    def active(self) -> bool:
        return this_year() <= self.until

    def __str__(self):
        items = [
            self.user.full_name_with_email,
            self.get_membership_type_display(),
            self.started,
        ]
        info = ', '.join(filter(None, map(str, items)))
        return info
