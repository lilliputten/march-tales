from .appEnv import (
    appEnv,
)

APP_NAME = 'tales_django'

DEFAULT_HOST = appEnv.str('DEFAULT_HOST', 'tales.march.team')
DEFAULT_FROM_EMAIL = appEnv.str('DEFAULT_FROM_EMAIL', 'info@' + DEFAULT_HOST)
