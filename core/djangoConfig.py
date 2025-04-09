from .appEnv import appEnv

# \<\(SECRET_KEY\|REGISTRATION_SALT\|EMAIL_HOST\|DEFAULT_FROM_EMAIL\|EMAIL_HOST_USER\|EMAIL_HOST_PASSWORD\)\>

APP_NAME = 'tales_django'

BASE_HOST = appEnv.str('BASE_HOST', 'march.team')
DEFAULT_HOST = appEnv.str('DEFAULT_HOST', 'tales.march.team')

# Folders

MEDIA_TRACKS_FOLDER = appEnv.str('MEDIA_TRACKS_FOLDER', 'tracks')

# Database setup
DB_ENGINE = appEnv.str('DB_ENGINE', 'django.db.backends.mysql')
DB_NAME = appEnv.str('DB_NAME', '')
DB_USER = appEnv.str('DB_USER', '')
DB_PASSWORD = appEnv.str('DB_PASSWORD', '')
DB_HOST = appEnv.str('DB_HOST', 'localhost')
DB_PORT = appEnv.str('DB_PORT', '5432')

# Email...

DEFAULT_FROM_EMAIL = appEnv.str('DEFAULT_FROM_EMAIL', 'tales@' + BASE_HOST)
EMAIL_HOST = appEnv.str('EMAIL_HOST', 'smtp.fullspace.ru')
EMAIL_PORT = appEnv.int('EMAIL_PORT', 465)   # 465 | 25
EMAIL_USE_SSL = appEnv.bool('EMAIL_USE_SSL', True)
EMAIL_USE_TLS = appEnv.bool('EMAIL_USE_TLS', False)

EMAIL_HOST_USER = appEnv.str('EMAIL_HOST_USER', 'tales@march.team')   # tales@march.team | goldenjeru
EMAIL_HOST_PASSWORD = appEnv.str('EMAIL_HOST_PASSWORD', '')

# OAath

# Google auth

GOOGLE_CLIENT_ID = appEnv.str('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = appEnv.str('GOOGLE_CLIENT_SECRET', '')

# Yandex auth

YANDEX_CLIENT_ID = appEnv.str('YANDEX_CLIENT_ID', '')
YANDEX_CLIENT_SECRET = appEnv.str('YANDEX_CLIENT_SECRET', '')
