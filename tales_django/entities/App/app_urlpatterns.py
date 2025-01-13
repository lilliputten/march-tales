from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403, handler500
from django.urls import include, path
from django.views.decorators.cache import cache_page

from .views import page403, page404, page500
from .api import api_urlpatterns

from .views import (
    index_view,
    RobotsView,
    components_demo,
    empty_demo,
)

cache_timeout = 0 if settings.LOCAL or settings.DEBUG else 15 * 60  # in seconds: {min}*60

app_urlpatterns = [
    # Root page
    path('', index_view, name='index'),
    # Core?
    # path('', include('pages.urls')),
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

app_urlpatterns += api_urlpatterns

# app_urlpatterns.append(url(r'^translations/', include(translation_urls)))
# app_urlpatterns.append(path(r'^translations/', translation_urls.urlpatterns))

app_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # @see https://www.django-rest-framework.org/
    path('api-auth/', include('rest_framework.urls')),
    # Demo pages (for debug/dev purposes only)...
    app_urlpatterns.append(
        path('components-demo', components_demo, name='components_demo'),
    )
    app_urlpatterns.append(
        path('empty-demo', empty_demo, name='empty_demo'),
    )

handler403 = page403   # 'tales_django.views.page403'
handler404 = page404   # 'tales_django.views.page404'
handler500 = page500   # 'tales_django.views.page500'

__all__ = [
    'app_urlpatterns',
    'handler403',
    'handler404',
    'handler500',
]
