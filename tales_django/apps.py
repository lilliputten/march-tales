from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.apps import AppConfig

# from translation_manager.signals import post_publish as translation_post_publish

from core.logging import getDebugLogger


_logger = getDebugLogger()

# def restart_server():
#     # TODO: Touch `index.wsgi`
#     _logger.info('restart_server')
#     pass


# translation_post_publish.connect(restart_server, sender=None)


class TalesConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD  # 'django.db.models.BigAutoField'
    name = 'tales_django'
    verbose_name = _('Application')

    def ready(self):
        # from .entities.Tracks.signals import on_track_delete
        return super().ready()
