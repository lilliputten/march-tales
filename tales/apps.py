from django.apps import AppConfig
from django.utils.functional import cached_property


class TalesConfig(AppConfig):
    default_auto_field = cached_property('django.db.models.BigAutoField')
    name = 'tales'
