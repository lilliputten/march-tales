from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.logging import getDebugLogger

_logger = getDebugLogger()


class TalesConfig(AppConfig):
    # default_site = 'tales_django.admin.AppAdminSite'

    default_auto_field = settings.DEFAULT_AUTO_FIELD  # 'django.db.models.BigAutoField'
    name = 'tales_django'
    verbose_name = _('Application')

    def ready(self):
        # from .entities.Tracks.signals import on_track_delete

        # # EXAMPLE: Register lower lookup for CharField
        # from django.db.models import CharField
        # from django.db.models.functions import Lower
        # CharField.register_lookup(Lower)

        return super().ready()
