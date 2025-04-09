# -*- coding:utf-8 -*-

import logging
import logging.handlers

from core.appEnv import LOCAL, appEnv

USE_LOGS_SERVER = appEnv.bool('USE_LOGS_SERVER', False)
USE_SYSLOG_SERVER = appEnv.bool('USE_SYSLOG_SERVER', False)

LOGGING_SERRVER_LOG_FILE = appEnv.str('LOGGING_SERRVER_LOG_FILE', 'logging-server.log')

SYSLOG_HOST = appEnv.str('SYSLOG_HOST', '127.0.0.1')
SYSLOG_PORT = appEnv.int('SYSLOG_PORT', '514')

LOGS_SERVER_PREFIX = appEnv.str('LOGS_SERVER_PREFIX', 'http://')  # 'https://' for remote logging
LOGS_SERVER_HOST = appEnv.str('LOGS_SERVER_HOST', '127.0.0.1')  # <NGROK-ADDR> for remote logging
LOGS_SERVER_PORT = appEnv.int('LOGS_SERVER_PORT', '5000')  # '443' for remote logging
LOGS_SERVER_RETRIES = appEnv.int('LOGS_SERVER_RETRIES', '0')
#  LOGS_SERVER_TOKEN = str(appConfig.get('LOGS_SERVER_TOKEN', '') # Could be used to provide basic authentification)

LOGS_SERVER_URL = LOGS_SERVER_PREFIX + LOGS_SERVER_HOST + ':' + str(LOGS_SERVER_PORT)

# Local logging

LOCAL_LOG_FILE = appEnv.str('LOCAL_LOG_FILE', 'log-local.log')


# Setup format
nameWidth = 20
nameFormat = '-' + str(nameWidth) + 's'

# Show time in log data
showLoggerTime = True

# Level (TODO: Make derived from a dev or prod environment?)
loggingLevel = logging.INFO   # INFO, DEBUG, CRITICAL etc

formatStr = ' '.join(
    list(
        filter(
            None,
            [
                # Combine log format string from items...
                '%(asctime)s' if showLoggerTime else None,
                '%(name)' + nameFormat,
                '%(levelname)-8s',
                '%(message)s',
            ],
        )
    )
)

__all__ = [
    'LOCAL',
    'USE_LOGS_SERVER',
    'USE_SYSLOG_SERVER',
    'LOGGING_SERRVER_LOG_FILE',
    'SYSLOG_HOST',
    'SYSLOG_PORT',
    'LOGS_SERVER_PREFIX',
    'LOGS_SERVER_HOST',
    'LOGS_SERVER_PORT',
    'LOGS_SERVER_RETRIES',
    #  'LOGS_SERVER_TOKEN',
    'LOGS_SERVER_URL',
    'nameWidth',
    'nameFormat',
    'showLoggerTime',
    'loggingLevel',
    'formatStr',
]
