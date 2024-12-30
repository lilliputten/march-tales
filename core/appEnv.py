# -*- coding:utf-8 -*-

import os
import pathlib
import posixpath

# import random
# import re
# import string
import environ

# from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
PROJECT_PATH = BASE_DIR.as_posix()
STATIC_PATH = posixpath.join(PROJECT_PATH, 'static')
print('BASE_DIR:', BASE_DIR)
print('PROJECT_PATH:', PROJECT_PATH)
print('STATIC_PATH:', STATIC_PATH)

PROJECT_INFO = ''
with open(posixpath.join(STATIC_PATH, 'project-info.txt')) as fh:
    info = fh.read()
    if info:
        PROJECT_INFO = info.strip()

appEnv = environ.FileAwareEnv(
    # @see local `.dev` file and example in `.dev.SAMPLE`
    # @see https://django-environ.readthedocs.io
    # @see https://django-environ.readthedocs.io/en/latest/tips.html
    LOCAL=(bool, False),
    DEBUG=(bool, False),
)

environ.Env.read_env(os.path.join(PROJECT_PATH, '.env'))
environ.Env.read_env(os.path.join(PROJECT_PATH, '.env.local'))
environ.Env.read_env(os.path.join(PROJECT_PATH, '.env.secure'))

LOCAL = appEnv.bool('LOCAL', False)
DEBUG = True if appEnv.bool('DEBUG', False) else LOCAL

WERKZEUG_RUN_MAIN = appEnv.bool('WERKZEUG_RUN_MAIN', False)
isNormalRun = not LOCAL or WERKZEUG_RUN_MAIN
