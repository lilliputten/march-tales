# -*- coding: utf-8 -*-

import os
import sys
import time
import traceback
import signal
from pathlib import Path

# @see https://docs.djangoproject.com/en/5.1/intro/tutorial02/

# App root path
rootPath = os.path.dirname(os.path.abspath(__file__))

# Detect home path...
home = str(Path.home())

activate_this = home + '/.venv-py3.11-django-5/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

sys.path.insert(1, rootPath)

import django

# TODO: To use `tales_django.settings`?
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "default_settings")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tales_django.settings')
from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
except RuntimeError:
    traceback.print_exc()
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(2.5)

