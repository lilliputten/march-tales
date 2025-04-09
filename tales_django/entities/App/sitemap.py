from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from tales_django.entities.Tracks.models import Rubric, Tag, Track
from tales_django.entities.Tracks.views import author_sitemap


class StaticSitemap(Sitemap):
    i18n = True
    changefreq = 'monthly'

    def items(self):
        return [
            'index',
            'tracks',
            'author_index',
            'rubric_index',
            'tag_index',
            'about',
            'application',
            'terms',
            'cookies-agreement',
            'privacy-policy',
        ]

    def location(self, item):
        return reverse(item)


class CustomFlatPageSitemap(FlatPageSitemap):
    changefreq = 'weekly'

    def lastmod(self, obj):
        return obj.flatpage.updated_at


# @see https://docs.djangoproject.com/en/5.1/ref/contrib/sitemaps/

# TODO:
# - Cache sitemaps.

sitemaps = {
    'static': StaticSitemap,
    'flatpages': CustomFlatPageSitemap,
    'tracks': GenericSitemap({'queryset': Track.objects.all(), 'date_field': 'updated_at'}, changefreq='weekly'),
    'authors': author_sitemap,
    'rubrics': GenericSitemap({'queryset': Rubric.objects.all(), 'date_field': 'updated_at'}, changefreq='weekly'),
    'tags': GenericSitemap({'queryset': Tag.objects.all(), 'date_field': 'updated_at'}, changefreq='weekly'),
}

sitemap_url = path(
    'sitemap.xml',
    sitemap,
    {'sitemaps': sitemaps},
    name='django.contrib.sitemaps.views.sitemap',
)

__all__ = [
    'sitemap_url',
]
