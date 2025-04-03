from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from ..models import Author

# from transcriber.models import PodcastGenre


class author_sitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        # Assuming you have a method to fetch episodes
        return Author.objects.all()

    def lastmod(self, obj):
        # Assuming you have a date field for last modification
        return obj.date_published
