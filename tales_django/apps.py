from django.apps import AppConfig

from tales_django import settings


class TalesConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD  # 'django.db.models.BigAutoField'
    name = 'tales_django'

    def ready(self):
        # from .entities.Tracks.signals import on_track_delete
        return super().ready()
