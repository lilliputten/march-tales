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


class User(AbstractUser):
    pass

# class User(AbstractUser):
#     username = models.CharField(max_length=50, blank=True, null=True, unique=True)
#     email = models.EmailField('email address', unique=True)
#     native_name = models.CharField(max_length=5)
#     phone_no = models.CharField(max_length=10)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
#
#     def __str__(self):
#         return '{}'.format(self.email)

    # # NOTE: It seems to be imposible to completely remove the `username` because it's used in django_registration
    # # username = None
    #
    # email = models.EmailField(unique=True)
    # address = models.TextField(blank=True, default='')
    #
    # # NOTE: Using the email field for the username is incompatible with `django_registration`:
    # # @see https://django-registration.readthedocs.io/en/3.4/custom-user.html#compatibility-of-the-built-in-workflows-with-custom-user-models
    # # The username and email fields must be distinct. If you wish to use the
    # # email address as the username, you will need to write your own completely
    # # custom registration form.
    #
    # # Username isn't used by itself, but it's still used in the django_registration internals. Both these fields are synced.
    #
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    #
    # # These variables are used to determine if email or username have changed on save
    # _original_email = None
    # _original_username = None
    #
    # class Meta(AbstractUser.Meta):
    #     #  # TODO: Add correct check if email and username are the same?
    #     #  constraints = [
    #     #      models.CheckConstraint(
    #     #          check=Q(email=models.F('username')),
    #     #          name='username_is_email',
    #     #      )
    #     #  ]
    #     pass
    #
    # def sync_email_and_username(self):
    #     # Check if email or username had changed?
    #     email_changed = self.email != self._original_email
    #     username_changed = self.username != self._original_username
    #     # Auto sync username and email
    #     if email_changed:
    #         self.username = self.email
    #     elif username_changed:
    #         self.email = self.username
    #     if email_changed or username_changed:
    #         self._original_email = self.email
    #         self._original_username = self.username
    #         # TODO: To do smth else if email has changed?
    #
    # def get_full_name_with_email(self):
    #     name = self.get_full_name()
    #     email = self.email
    #     if not name and email:
    #         name = email
    #     items = [
    #         name,
    #         '<{}>'.format(email) if email and email != name else '',
    #     ]
    #     info = '  '.join(filter(None, map(str, items)))
    #     return info
    #
    # @property
    # def full_name_with_email(self):
    #     return self.get_full_name_with_email()
    #
    # def clean(self):
    #     self.sync_email_and_username()
    #     return super().clean()
    #
    # def save(self, *args, **kwargs):
    #     self.sync_email_and_username()
    #     return super().save(*args, **kwargs)
    #
    # @property
    # def is_member(self) -> bool:
    #     try:
    #         return Membership.objects.get(user=self).active
    #     except ObjectDoesNotExist:
    #         return False
    #
    # def __init__(self, *args, **kwargs):
    #     super(User, self).__init__(*args, **kwargs)
    #     self._original_email = self.email
    #     self._original_username = self.username
    #
    # def email_user(
    #     self,
    #     subject: str,
    #     message: str,
    #     html_content: bool = False,
    #     attachment_content: FPDF | None = None,
    #     attachment_name: str | None = None,
    #     from_email: str | None = settings.DEFAULT_FROM_EMAIL,
    # ) -> None:
    #     send_email(
    #         recipient_address=self.email,
    #         subject=subject,
    #         message=message,
    #         pdf=attachment_content,
    #         pdf_name=attachment_name,
    #     )
    #