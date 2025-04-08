from django import forms
from django.conf import settings

from tales_django.core.widgets import textAreaWidget, textInputWidget
from tales_django.entities.Membership.models.Membership import MEMBERSHIP_DATA

# from ..models import MEMBERSHIP_DATA


class MembershipForm(forms.Form):
    name = forms.CharField(
        label='Name on invoice',
        max_length=100,
        widget=textInputWidget,
        help_text='In case it needs to be different on the invoice or receipt.',
        required=True,
    )
    address = forms.CharField(label='Address on invoice', widget=textAreaWidget, required=True)
    extra = forms.CharField(
        label='Extra invoice text details, like reference or purchase order numbers. Support Latin, Cyrillic and Greek scripts, but not emojis.',
        widget=textAreaWidget,
        required=False,
    )
    membership_type = forms.ChoiceField(
        choices=MEMBERSHIP_DATA.public_choice_field_with_prices,
        widget=forms.RadioSelect,
        required=True,
        label='Membership type',
    )
    # # TODO: Payments subsystem
    # payment_method = forms.ChoiceField(
    #     choices=Payment.METHODS,
    #     required=True,
    #     label="Payment method",
    #     # See stylization in `src/assets/common/fix-django-forms.scss`, by option element' id.
    #     widget=forms.RadioSelect,
    # )
    mailing_list = forms.BooleanField(
        initial=True,
        label=f'Send me the {settings.SITE_SHORT_NAME} newsletter, and emails about {settings.SITE_SHORT_NAME} events, courses, and online seminars',
    )
