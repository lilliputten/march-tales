from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clear django cache'

    def handle(self, *args, **kwargs):
        cache.clear()
        self.stdout.write('Cache is cleared\n')
