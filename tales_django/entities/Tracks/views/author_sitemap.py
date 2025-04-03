from django.contrib.sitemaps import Sitemap

from ..models import Author

# @see https://docs.djangoproject.com/en/5.1/ref/contrib/sitemaps/


class author_sitemap(Sitemap):
    changefreq = 'weekly'
    # priority = 0.6

    def items(self):
        return Author.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
