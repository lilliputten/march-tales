# @module models.py
# @changed 2024.03.28, 19:28
# type: ignore[attr-defined]

import random
import string
from datetime import date
import requests

# from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Model, Q, QuerySet
from django.urls import reverse
from fpdf import FPDF

from core.helpers.dates import this_year

from tales_django.core.constants.payments import (
    site_default_currency,
    site_supported_currencies,
)

from ..core.constants.date_time_formats import dateFormat
from ..core.constants.payments import currency_emojis, payment_details_by_currency

# from .core.helpers.create_pdf import (
#     create_invoice_pdf_from_payment,
#     create_receipt_pdf_from_payment,
# )
from ..core.helpers.email import send_email


alphabet = string.ascii_lowercase + string.digits
random_code_length = 8


# NOTE: A single reusable QuerySet to check if the registration active
REGISTRATION_ACTIVE_QUERY = ~Q(status__in=('CANCELLED', 'WITHDRAWN', 'DECLINED'))


def random_code(length=random_code_length):
    return ''.join(random.choices(alphabet, k=length))


class MembershipData:
    data = [
        {
            'tag': 'ACADEMIC',
            'label': 'Academic',
            'price': 25,
            'currency': 'EUR',
        },
        {
            'tag': 'NORMAL',
            'label': 'Normal',
            'price': 50,
            'currency': 'EUR',
            'default': True,
        },
        {
            'tag': 'HONORARY',
            'label': 'Honorary',
            'price': 0,
            'currency': 'EUR',
        },
    ]
    default = 'NORMAL'
    available = {'NORMAL', 'ACADEMIC'}

    def __getitem__(self, key: str) -> dict:
        dct = {o['tag']: o for o in self.data}
        return dct[key]

    @property
    def choices(self):
        return [(o['tag'], o['label']) for o in self.data]

    @property
    def public_choice_field_with_prices(self):
        return [
            (obj['tag'], '{} ({} {})'.format(obj['label'], obj['price'], obj['currency']))
            for obj in self.data
            if obj['tag'] in self.available
        ]


MEMBERSHIP_DATA = MembershipData()


class Membership(Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    membership_type = models.TextField(choices=MEMBERSHIP_DATA.choices, default=MEMBERSHIP_DATA.default)

    started = models.IntegerField(default=this_year)
    until = models.IntegerField(default=this_year)
    # payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
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
