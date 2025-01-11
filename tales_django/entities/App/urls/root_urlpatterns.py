from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403, handler500
from django.urls import include, path
from django.views.decorators.cache import cache_page

from tales_django.entities.App.views import page403, page404, page500

# from translation_manager import urls as translation_urls

from ..views import (
    index_view,
    RobotsView,
    components_demo,
    empty_demo,
)

cache_timeout = 0 if settings.LOCAL or settings.DEBUG else 15 * 60  # in seconds: {min}*60

root_urlpatterns = [
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

# root_urlpatterns.append(url(r'^translations/', include(translation_urls)))
# root_urlpatterns.append(path(r'^translations/', translation_urls.urlpatterns))


root_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Demo pages (for debug/dev purposes only)...
    root_urlpatterns.append(
        path('components-demo', components_demo, name='components_demo'),
    )
    root_urlpatterns.append(
        path('empty-demo', empty_demo, name='empty_demo'),
    )
    # root_urlpatterns += patterns(
    #     '',
    #     # url(r'^400/$', TemplateView.as_view(template_name='400.html.django')),
    #     url(r'^403/$', TemplateView.as_view(template_name='403.html.django')),
    #     url(r'^404/$', 'django.views.defaults.page_not_found'),
    #     url(r'^500/$', 'django.views.defaults.server_error'),
    # )
# else:
#     handler404 = page404
#     # handler403 = views.page403
#     # handler404 = views.page404
#     # handler500 = views.page500
#

# root_urlpatterns.append(
#     path(r'^404/$', 'django.views.defaults.page_not_found')
# )

handler403 = 'tales_django.views.page403'
handler404 = page404   # 'tales_django.views.page404'
handler500 = 'tales_django.views.page500'

__all__ = [
    'handler403',
    'handler404',
    'handler500',
]
