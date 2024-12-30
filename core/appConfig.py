# -*- coding:utf-8 -*-

import os
import pathlib
import posixpath
import random
import re
import string
import environ
# from dotenv import dotenv_values


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
PROJECT_PATH = BASE_DIR.as_posix()
STATIC_PATH = posixpath.join(PROJECT_PATH, 'static')
print("BASE_DIR:", BASE_DIR)
print("PROJECT_PATH:", PROJECT_PATH)
print("STATIC_PATH:", STATIC_PATH)

with open(posixpath.join(STATIC_PATH, 'project-info.txt')) as fh:
    info = fh.read()
    if info:
        PROJECT_INFO = info.strip()

appEnv = environ.Env(
    # @see local `.dev` file and example in `.dev.SAMPLE`
    # @see https://django-environ.readthedocs.io
    LOCAL=(bool, False),
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    REGISTRATION_SALT=(str, ''),
    DEFAULT_FROM_EMAIL=(str, 'info@tales.march.team'),
    WERKZEUG_RUN_MAIN=(bool, False),
    TZ_HOURS_OFFSET=(int, 0),
    # SENDGRID_API_KEY=(str, ''),
    # STRIPE_PUBLISHABLE_KEY=(str, ''),
    # STRIPE_SECRET_KEY=(str, ''),
    # SLACK_WEBHOOK=(str, ''),
    # Other parameters
    **{
        'PROJECT_INFO': PROJECT_INFO,
        # Paths...
        'PROJECT_PATH': PROJECT_PATH,
        'STATIC_PATH': STATIC_PATH,
    },
)

environ.Env.read_env(os.path.join(PROJECT_PATH, '.env'))
environ.Env.read_env(os.path.join(PROJECT_PATH, '.env.local'))
environ.Env.read_env(os.path.join(PROJECT_PATH, '.env.secure'))

# appConfig = {
#     **dotenv_values('.env'),
#     **dotenv_values('.env.local'),
#     **dotenv_values('.env.secure'),
#     # Override loaded values with environment variables
#     **os.environ,
#     # Other parameters
#     **{
#         # DEBUG: Changed timestamp
#         'PROJECT_INFO': PROJECT_INFO,
#         # Paths...
#         'PROJECT_PATH': PROJECT_PATH,
#         'STATIC_PATH': STATIC_PATH,
#     },
# }


LOCAL = bool(appEnv('LOCAL'))
DEBUG = True if bool(appEnv('DEBUG')) else LOCAL

WERKZEUG_RUN_MAIN = bool(appEnv('WERKZEUG_RUN_MAIN'))
isNormalRun = not LOCAL or WERKZEUG_RUN_MAIN

# Timezone (set `TZ_HOURS` to hours value to adjust date representation to corresponding timezone)
TZ_HOURS = appEnv('TZ_HOURS_OFFSET')

# # Secrets
# # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(str(appEnv('SECRET_KEY')))
# REGISTRATION_SALT = str(str(appEnv('REGISTRATION_SALT')))
# # SENDGRID_API_KEY = str(str(appEnv('SENDGRID_API_KEY')))
# # STRIPE_PUBLISHABLE_KEY = str(str(appEnv('STRIPE_PUBLISHABLE_KEY')))
# # STRIPE_SECRET_KEY = str(str(appEnv('STRIPE_SECRET_KEY')))
# # SLACK_WEBHOOK = str(str(appEnv('SLACK_WEBHOOK')))
#
# SECRETS = [
#     (SECRET_KEY, 'SECRET_KEY'),
#     (REGISTRATION_SALT, 'REGISTRATION_SALT'),
#     # (SENDGRID_API_KEY, 'SENDGRID_API_KEY'), # EMAIL_HOST_PASSWORD
#     # (STRIPE_PUBLISHABLE_KEY, 'STRIPE_PUBLISHABLE_KEY'),
#     # (STRIPE_SECRET_KEY, 'STRIPE_SECRET_KEY'),
# ]
#
print("SECRET_KEY:", SECRET_KEY)
#
# def random_string(length: int = 32) -> str:
#     possibles = string.ascii_letters + string.digits
#     return ''.join(random.sample(possibles, length))
#
#
# # Check all the secrets...
# for key, label in SECRETS:
#     if not key:
#         if LOCAL and key in (SECRET_KEY, REGISTRATION_SALT):
#             key = random_string()
#         else:
#             error_text = f'Error: Environment configuration variable {label} is missing'
#             raise Exception(error_text)
#
#
