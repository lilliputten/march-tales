from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from ..models import Author

# @see https://docs.djangoproject.com/en/5.1/ref/contrib/sitemaps/


class author_sitemap(Sitemap):
    # changefreq = 'daily'
    # priority = 0.6

    def items(self):
        return Author.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    # def location(self, item):
    #     # if kwargs not in item set as None
    #     kwargs = item['kwargs'] if 'kwargs' in item else None
    #     return reverse(item['view_name'], kwargs=kwargs)
