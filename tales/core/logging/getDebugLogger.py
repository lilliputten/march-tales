# -*- coding:utf-8 -*-

import os
import logging
import logging.handlers
import pathlib
import posixpath


def getDebugLogger(id: str | None = None):
    if not id:
        # Create deafault id - for the parent module, with deep=True getModulePath parameter
        id = getModulePath(True)
    logger = logging.getLogger(id)
    # Default handler (console)...
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(loggerConfig.loggingLevel)
    consoleHandler.formatter = _defaultFormatter
    # Add local file logger
    if loggerConfig.LOCAL_LOG_FILE and not IS_VERCEL:
        cwd = pathlib.Path(os.getcwd()).as_posix()
        localLogFileHandler = ConcurrentRotatingFileHandler(
            # @see:
            # - https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler
            # - [logging - Rotating file handler gives error in python logw](https://stackoverflow.com/questions/68253737/rotating-file-handler-gives-error-in-python-log/77394567#77394567)
            filename=posixpath.join(cwd, loggerConfig.LOCAL_LOG_FILE),
            mode='a',
            encoding='utf-8',
            maxBytes=100000,
            backupCount=5,
            #  delay=True,
            #  errors=True,
        )  # max log file size 100 MB
        localLogFileHandler.setFormatter(_noColorFormatter)
        localLogFileHandler.setLevel(loggerConfig.loggingLevel)
        localLogFileHandler.formatter = _noColorFormatter
        localLogFileHandler.level = loggerConfig.loggingLevel
        logger.addHandler(localLogFileHandler)
    # Syslog, @see https://docs.python.org/3/library/logging.handlers.html#sysloghandler
    if loggerConfig.USE_SYSLOG_SERVER:
        syslogHandler = logging.handlers.SysLogHandler(
            address=(loggerConfig.SYSLOG_HOST, loggerConfig.SYSLOG_PORT),
        )
        syslogHandler.setLevel(loggerConfig.loggingLevel)
        syslogHandler.formatter = _defaultFormatter
        logger.addHandler(syslogHandler)
    #  if useDebugLogs: # DEBUG
    #     addDebugLog('getDebugLogger %s USE_LOGS_SERVER: %s' % (id, USE_LOGS_SERVER))
    # Create a custom http logger handler
    if loggerConfig.USE_LOGS_SERVER:
        httpHandler = CustomHttpHandler(
            url=loggerConfig.LOGS_SERVER_URL,
            #  token=LOGS_SERVER_TOKEN,
            #  silent=False,
        )
        httpHandler.setLevel(loggerConfig.loggingLevel)
        httpHandler.setFormatter(customHttpHandlerFormatter)
        logger.addHandler(httpHandler)
    logger.setLevel(loggerConfig.loggingLevel)
    return logger
