from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from django.views.decorators.cache import cache_page

# from translation_manager import urls as translation_urls

from ..views import (
    index,
    RobotsView,
    components_demo,
)

cache_timeout = 0 if settings.LOCAL or settings.DEBUG else 15 * 60  # in seconds: {min}*60

root_urlpatterns = [
    # Root page
    path('', index, name='index'),
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
    # App-provided paths...
    path('admin/', admin.site.urls, name='admin'),
    # Service pages...
    path(
        'robots.txt',
        cache_page(cache_timeout)(RobotsView.as_view()),
        name='robots',
    ),
]

# root_urlpatterns.append(url(r'^translations/', include(translation_urls)))
# root_urlpatterns.append(path(r'^translations/', translation_urls.urlpatterns))


root_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Demo pages (for debug/dev purposes only)...
    root_urlpatterns.append(
        path('components-demo', components_demo, name='components_demo'),
    )
