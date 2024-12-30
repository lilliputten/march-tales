import os
import pathlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tales_django.settings')
from django.core.management import execute_from_command_line


def clean_db():
    """
    rm -f db.sqlite3
    """
    print('Django remove database...')
    pathlib.Path('db.sqlite3').unlink(missing_ok=True)
    print('Done')


def migrate():
    """
    python manage.py migrate
    """
    print('Django migrate...')
    execute_from_command_line(['manage.py', 'migrate'])
    print('Done')


def superuser():
    """
    python manage.py createsuperuser --username admin --email dmia@yandex.ru
    """
    print('Create superuser...')
    execute_from_command_line(
        [
            'manage.py',
            'createsuperuser',
            '--username',
            'admin',
            '--email',
            'dmia@yandex.ru',
        ]
    )
    print('Done')


def runserver():
    """
    python manage.py runserver
    """
    # NOTE: It can't run this way
    execute_from_command_line(['manage.py', 'runserver'])


def livereload():
    """
    python manage.py livereload
    """
    # NOTE: It can't run this way
    execute_from_command_line(['manage.py', 'livereload'])


def shell():
    """
    python manage.py shell
    """
    # NOTE: It can't run this way
    execute_from_command_line(['manage.py', 'shell'])
