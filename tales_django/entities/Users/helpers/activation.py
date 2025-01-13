# @module tales_django/views/helpers.py
# @changed 2024.04.04, 20:27

import traceback

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpRequest
from django.template.loader import render_to_string

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger

# For django_registration related stuff, see:
# .venv/Lib/site-packages/django_registration/backends/activation/views.py

REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')

logger = getDebugLogger()


def get_activation_key(user: AbstractBaseUser | AnonymousUser):
    """
    Generate the activation key which will be emailed to the user.
    Adopted from: .venv/Lib/site-packages/django_registration/backends/activation/views.py
    """
    return signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)


def get_email_context(request: HttpRequest, activation_key: str):
    """
    Build the template context used for the activation email.
    Adopted from: .venv/Lib/site-packages/django_registration/backends/activation/views.py
    """
    scheme = 'https' if request.is_secure() else 'http'
    return {
        'scheme': scheme,
        'activation_key': activation_key,
        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        'site': get_current_site(request),
    }


def send_re_actvation_email(request: HttpRequest, user: AbstractBaseUser | AnonymousUser):
    """
    Send the activation email. The activation key is the username,
    signed using TimestampSigner.
    Adopted from: .venv/Lib/site-packages/django_registration/backends/activation/views.py
    """
    try:
        # TODO: Use changed for the re-activate case template?
        email_body_template = 'django_registration/activation_email_body.txt'
        email_subject_template = 'django_registration/activation_email_subject.txt'
        activation_key = get_activation_key(user)
        context = get_email_context(request, activation_key)
        context['user'] = user

        subject = render_to_string(
            template_name=email_subject_template,
            context=context,
            request=request,
        )
        # Force subject to a single line to avoid header-injection issues.
        subject = ''.join(subject.splitlines()).strip()
        message = render_to_string(
            template_name=email_body_template,
            context=context,
            request=request,
        )
        user.email_user(subject, message)
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        debugData = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error(f'Caught error {sError} (re-raising):\n{debugObj(debugData)}')
        raise err
