from django.apps import AppConfig

from tales import settings


class TalesConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD  # 'django.db.models.BigAutoField'
    name = 'tales'
