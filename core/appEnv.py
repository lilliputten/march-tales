# -*- coding:utf-8 -*-

import os
import pathlib
import posixpath
import environ

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
PROJECT_PATH = BASE_DIR.as_posix()
STATIC_FOLDER = 'static'
STATIC_ROOT = posixpath.join(PROJECT_PATH, STATIC_FOLDER)
MEDIA_FOLDER = 'media'
MEDIA_ROOT = posixpath.join(PROJECT_PATH, MEDIA_FOLDER)

SRC_FOLDER = 'src'
SRC_ROOT = posixpath.join(BASE_DIR, SRC_FOLDER)
ASSETS_FOLDER = 'assets'
ASSETS_ROOT = posixpath.join(SRC_FOLDER, ASSETS_FOLDER)

# print('BASE_DIR:', BASE_DIR)
# print('PROJECT_PATH:', PROJECT_PATH)
# print('STATIC_ROOT:', STATIC_ROOT)

PROJECT_INFO = ''
with open(posixpath.join(STATIC_ROOT, 'project-info.txt')) as fh:
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

# Should be provided by vercel environment for production
VERCEL_URL = appEnv.str('VERCEL_URL', '')
IS_VERCEL = True if VERCEL_URL else False

# Temp path: Use local 'temp' or vercel specific '/tmp' folders for temporary files
# TEMP_PATH = posixpath.join(PROJECT_PATH, '.temp') if LOCAL or not IS_VERCEL else '/tmp'
TEMP_PATH = posixpath.join(PROJECT_PATH, '.temp')
# Set temp path location for django
os.environ['TMPDIR'] = TEMP_PATH
pathlib.Path(TEMP_PATH).mkdir(
    parents=True,
    exist_ok=True,
    mode=0o777,
)
