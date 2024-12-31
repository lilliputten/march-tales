from .appEnv import (
    appEnv,
)

APP_NAME = 'tales_django'

BASE_HOST = appEnv.str('BASE_HOST', 'march.team')
DEFAULT_HOST = appEnv.str('DEFAULT_HOST', 'tales.march.team')
DEFAULT_FROM_EMAIL = appEnv.str('DEFAULT_FROM_EMAIL', 'tales@' + BASE_HOST)

EMAIL_HOST = appEnv.str('EMAIL_HOST', 'smtp.fullspace.ru')
EMAIL_HOST_USER = appEnv.str('EMAIL_HOST_USER', 'tales@march.team')
EMAIL_HOST_PASSWORD = appEnv.str('EMAIL_HOST_PASSWORD', '')
