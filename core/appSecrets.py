# -*- coding:utf-8 -*-

import random
import string

from core.appEnv import appEnv, LOCAL

# Secrets
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(appEnv.str('SECRET_KEY', ''))
REGISTRATION_SALT = str(appEnv.str('REGISTRATION_SALT', ''))
# SENDGRID_API_KEY = str(appEnv.str('SENDGRID_API_KEY', ''))
# STRIPE_PUBLISHABLE_KEY = str(appEnv.str('STRIPE_PUBLISHABLE_KEY', ''))
# STRIPE_SECRET_KEY = str(appEnv.str('STRIPE_SECRET_KEY', ''))
# SLACK_WEBHOOK = str(appEnv.str('SLACK_WEBHOOK', ''))

SECRETS = [
    (SECRET_KEY, 'SECRET_KEY'),
    (REGISTRATION_SALT, 'REGISTRATION_SALT'),
    # (SENDGRID_API_KEY, 'SENDGRID_API_KEY'), # EMAIL_HOST_PASSWORD
    # (STRIPE_PUBLISHABLE_KEY, 'STRIPE_PUBLISHABLE_KEY'),
    # (STRIPE_SECRET_KEY, 'STRIPE_SECRET_KEY'),
]

print('SECRET_KEY:', SECRET_KEY)


def random_string(length: int = 32) -> str:
    possibles = string.ascii_letters + string.digits
    return ''.join(random.sample(possibles, length))


# Check all the secrets...
for key, label in SECRETS:
    if not key:
        if LOCAL and key in (SECRET_KEY, REGISTRATION_SALT):
            key = random_string()
        else:
            error_text = f'Error: Environment configuration variable {label} is missing'
            raise Exception(error_text)
