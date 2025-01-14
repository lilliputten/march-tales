# -*- coding: utf-8 -*-
"""
Django settings for tales project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/

@changed 2025.01.03, 20:54
"""

import posixpath

from core.appEnv import (
    BASE_DIR,
    LOCAL,
    DEBUG,
    STATIC_FOLDER,
    STATIC_ROOT,
    MEDIA_FOLDER,
    MEDIA_ROOT,
    SRC_ROOT,
    ASSETS_ROOT,
    PROJECT_INFO,  # DEBUG
)
from core.appSecrets import (
    SECRET_KEY,
    REGISTRATION_SALT,
    # SENDGRID_API_KEY,
    # STRIPE_PUBLISHABLE_KEY,
    # STRIPE_SECRET_KEY,
    # SLACK_WEBHOOK,
)
from core.djangoConfig import (
    APP_NAME,
    DEFAULT_HOST,
    # Email...
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USE_TLS,
    EMAIL_USE_SSL,
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
)

# TRANSLATIONS_PROJECT_BASE_DIR = BASE_DIR

gettext = lambda s: s

# # DEBUG: Show basic settings...
# print('App started:', PROJECT_INFO)
# print('EMAIL_HOST:', EMAIL_HOST)
# print('EMAIL_PORT:', EMAIL_PORT)
# print('EMAIL_USE_TLS:', EMAIL_USE_TLS)
# print('EMAIL_USE_SSL:', EMAIL_USE_SSL)
# print('DEFAULT_FROM_EMAIL:', DEFAULT_FROM_EMAIL)
# print('EMAIL_HOST_USER:', EMAIL_HOST_USER)
# print('EMAIL_HOST_PASSWORD:', EMAIL_HOST_PASSWORD)
# print('REGISTRATION_SALT:', REGISTRATION_SALT)

# Define default site id for `sites.models`
SITE_ID = 1

STATIC_URL = f'/{STATIC_FOLDER}/'
MEDIA_URL = f'/{MEDIA_FOLDER}/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

if LOCAL:
    # Add asset file sources to static folders in dev mode to access scss sources via django filters during dev mode time
    STATICFILES_DIRS += (SRC_ROOT,)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    # ('text/x-scss', 'sass --embed-source-map {infile} {outfile}'),
    # Sass installation:
    # - https://sass-lang.com/install/
    # - https://github.com/sass/dart-sass/releases/latest
    # @see https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_PRECOMPILERS
)

FILE_UPLOAD_HANDLERS = (
    # TemporaryFileUploadHandler is required for processing uploaded audios with ffmpeg
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

ALLOWED_HOSTS = [
    DEFAULT_HOST,
]
CSRF_TRUSTED_ORIGINS = [
    'https://' + DEFAULT_HOST,
]

if LOCAL:
    # Allow work with local server in local dev mode
    ALLOWED_HOSTS.append('localhost')

# Application definition

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # Added
    # 'modeltranslation',  # XXX: Doesn't work in django 5?
    # 'translation_manager',
    'translated_fields',
    'compressor',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_registration',
    'rest_framework',
    APP_NAME,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Added
    APP_NAME + '.middleware.BeautifulMiddleware.BeautifulMiddleware',  # Html content prettifier
]

# Add livereload app...
# @see https://pypi.org/project/django-livereload/
# @see https://github.com/tjwalch/django-livereload-server
# Run the reload server with a command: `python manage.py livereload src static`
INSTALLED_APPS.insert(0, 'livereload')
if DEBUG:
    MIDDLEWARE.insert(0, 'livereload.middleware.LiveReloadScript')
    # MIDDLEWARE.append('livereload.middleware.LiveReloadScript')
# TODO: Do we actually need livereload in production? I remember some issues with it. Can we completely remove it from production?
# There is already present the check in the `tales_django/templates/base-core.html.django` template:
# ```
#  {% if settings.DEBUG %}
#  {% load livereload_tags %}
#  {% endif %}
# ```

ROOT_URLCONF = APP_NAME + '.urls'

# Templates folders...
APP_TEMPLATES_PATH = BASE_DIR / APP_NAME / 'templates'

TEMPLATE_DIRS = [
    APP_TEMPLATES_PATH,
    SRC_ROOT,  # To access template include blocks
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                APP_NAME + '.core.app.context_processors.common_values',
            ],
        },
        'DIRS': TEMPLATE_DIRS,
    },
]

WSGI_APPLICATION = APP_NAME + '.wsgi.application'

# @see https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'index'

# Registration
# @see https://django-registration.readthedocs.io

AUTH_USER_MODEL = APP_NAME + '.User'
AUTHENTICATION_BACKENDS = [
    APP_NAME + '.core.app.backends.EmailBackend',  # TODO?
]

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window

# NOTE: It's possible to store some of these parameters (`DEFAULT_FROM_EMAIL`, definitely) in the site preferences or in the `.env*` files
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = str(env('DEFAULT_FROM_EMAIL'))
# EMAIL_HOST = DEFAULT_EMAIL_HOST if DEFAULT_EMAIL_HOST else 'smtp.fullspace.ru'
# EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
# EMAIL_PORT = 25 # 465
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = False
# @see https://docs.sendgrid.com/for-developers/sending-email/django
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY

# Internationalization
# @see https://docs.djangoproject.com/en/5.1/topics/i18n/
# @see https://docs.djangoproject.com/en/5.1/topics/i18n/translation/
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'   # 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (posixpath.join(BASE_DIR, APP_NAME, 'locale'),)
LANGUAGES = (
    ('ru', 'Русский'),
    # ('fr', gettext(u'Français')),
    ('en', 'English'),
)
LANGUAGES_LIST = {lng: name for lng, name in list(LANGUAGES)}
CMS_LANGUAGES = {
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': lng,
            'hide_untranslated': False,
            'name': name,
            'redirect_on_fallback': True,
        }
        for lng, name in list(LANGUAGES)
    ],
}

# @see: https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#std:templatefilter-date
DATE_FORMAT = 'Y.m.d'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = DATE_FORMAT + ',' + TIME_FORMAT

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging

# Performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#
# Logging levels:
#
# - DEBUG: Low level system information for debugging purposes
# - INFO: General system information
# - WARNING: Information describing a minor problem that has occurred.
# - ERROR: Information describing a major problem that has occurred.
# - CRITICAL: Information describing a critical problem that has occurred.
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'incremental': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)s:%(lineno)s %(levelname)s %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S',
        },
        'simple': {'format': '%(levelname)s %(message)s'},
    },
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'errors': {
            'level': 'ERROR',
            'filename': posixpath.join(BASE_DIR, 'log-errors.log'),
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024,  # MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'django': {
            'level': 'DEBUG',
            'filename': posixpath.join(BASE_DIR, 'log-django.log'),
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024,  # MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'apps': {
            'level': 'DEBUG',
            'filename': posixpath.join(BASE_DIR, 'log-apps.log'),
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024,  # MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': [
                'errors',
                # 'mail_admins',
            ],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['django'],
            'propagate': True,
            'level': 'INFO',
        },
        APP_NAME: {
            'handlers': ['apps'],
            'level': 'DEBUG',
        },
    },
}
ADMINS = (('ME', 'lilliputten@gmail.com'),)
MANAGERS = ADMINS

# @see: https://docs.djangoproject.com/en/2.0/ref/settings/#timeout
TIMEOUT = 30 if DEBUG else 300  # Short value for cache expiration

# Site config

# TODO: Use `Site.objects.get_current().name` (via `from django.contrib.sites.models import Site`) as site title.
SITE_NAME = 'March Tales'
# TODO: Add proper site description and keywords...
# SITE_DESCRIPTION = 'March Tales django api and web frontend server'
# SITE_KEYWORDS = """
# march
# tales
# """

SITE_SHORT_NAME = SITE_NAME

# Pass settings to templates' context, see `tales_django/core/app/context_processors.py`...
PASS_VARIABLES = {
    'DEBUG': DEBUG,  # Pass django debug flag to the code (from environment)
    'LOCAL': LOCAL,  # Local dev server mode (from the environment)
    'PROJECT_INFO': PROJECT_INFO,
    'DEFAULT_HOST': DEFAULT_HOST,
    'GITHUB': 'https://github.com/lilliputten/march-tales',
    'SECRET_KEY': SECRET_KEY,
    'REGISTRATION_SALT': REGISTRATION_SALT,
    'USE_DJANGO_PREPROCESSORS': False,  # Preprocess scss source files with django filters, UNUSED
    # 'STRIPE_PUBLISHABLE_KEY': STRIPE_PUBLISHABLE_KEY,
    'DEFAULT_FROM_EMAIL': DEFAULT_FROM_EMAIL,
    'CONTACT_EMAIL': DEFAULT_FROM_EMAIL,
    # NOTE: Site url and name could be taken from site data via `get_current_site`
    'SITE_NAME': SITE_NAME,  # Use `{% trans 'Site title' %}
    'SITE_SHORT_NAME': SITE_SHORT_NAME,  # Use `{% trans 'Short site title' %}
    # 'SITE_TITLE': SITE_NAME,
    # 'SITE_DESCRIPTION': SITE_DESCRIPTION, # Use `{% trans 'Site description' %}
    # 'SITE_KEYWORDS': re.sub(r'\s*[\n\r]+\s*', ', ', SITE_KEYWORDS.strip()), # Use `{% trans 'Site keywords' %}
    'STATIC_URL': STATIC_URL,
    'MEDIA_URL': MEDIA_URL,
    # i18n
    'LANGUAGES': LANGUAGES,
    'LANGUAGES_LIST': LANGUAGES_LIST,
    'LANGUAGE_CODE': LANGUAGE_CODE,
}

__all__ = [
    # Email...
    'EMAIL_HOST',
    'EMAIL_PORT',
    'EMAIL_USE_TLS',
    'EMAIL_USE_SSL',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
    'DEFAULT_FROM_EMAIL',
    'SERVER_EMAIL',
    # Folders...
    'ASSETS_ROOT',
    'MEDIA_FOLDER',
    'MEDIA_ROOT',
    'MEDIA_URL',
    # 'SRC_ROOT',
    'STATIC_FOLDER',
    'STATIC_ROOT',
    'STATIC_URL',
]
