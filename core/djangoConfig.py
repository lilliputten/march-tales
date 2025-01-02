from .appEnv import (
    appEnv,
)

# \<\(SECRET_KEY\|REGISTRATION_SALT\|EMAIL_HOST\|DEFAULT_FROM_EMAIL\|EMAIL_HOST_USER\|EMAIL_HOST_PASSWORD\)\>

APP_NAME = 'tales_django'

BASE_HOST = appEnv.str('BASE_HOST', 'march.team')
DEFAULT_HOST = appEnv.str('DEFAULT_HOST', 'tales.march.team')

# Folders

MEDIA_TRACKS_FOLDER = appEnv.str('MEDIA_TRACKS_FOLDER', 'tracks')

# Email...

DEFAULT_FROM_EMAIL = appEnv.str('DEFAULT_FROM_EMAIL', 'tales@' + BASE_HOST)
EMAIL_HOST = appEnv.str('EMAIL_HOST', 'smtp.fullspace.ru')
EMAIL_PORT = appEnv.int('EMAIL_PORT', 465)   # 465 | 25
EMAIL_USE_SSL = appEnv.bool('EMAIL_USE_SSL', True)
EMAIL_USE_TLS = appEnv.bool('EMAIL_USE_TLS', False)

EMAIL_HOST_USER = appEnv.str('EMAIL_HOST_USER', 'tales@march.team')   # tales@march.team | goldenjeru
EMAIL_HOST_PASSWORD = appEnv.str('EMAIL_HOST_PASSWORD', '')
