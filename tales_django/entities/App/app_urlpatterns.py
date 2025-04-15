from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView

from tales_django.sites import unfold_admin_site

from .api import app_api_urlpatterns
from .sitemap import sitemap_url
from .views import RobotsView  # about_view,; application_view,
from .views import (
    components_demo,
    cookies_agreement_view,
    empty_demo,
    index_view,
    page403,
    page404,
    page500,
    privacy_policy_view,
    terms_view,
)

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

cache_timeout = 0 if settings.LOCAL or settings.DEBUG else 15 * 60  # in seconds: {min}*60

admin.site.site_header = _('Site administration')

app_urlpatterns = [
    # Root page
    path(r'', index_view, name='index'),
    path(r'tracks/', index_view, name='tracks'),  # TODO: Create dedicated view in tracks.
    # Secondary & static pages
    # path(r'about/', about_view, name='about'),
    # path(r'about/', RedirectView.as_view(url='/pages/about/', permanent=True)),
    # path(r'application-old/', application_view, name='application'),
    path(r'terms/', terms_view, name='terms'),
    path(r'cookies-agreement/', cookies_agreement_view, name='cookies-agreement'),
    path(r'privacy-policy/', privacy_policy_view, name='privacy-policy'),
    # Pages
    # path('', include('pages.urls')),
    # tales_django/entities/flatpages/urls.py
    path(r'/', include('tales_django.entities.flatpages.urls'), name='django.contrib.flatpages.views.flatpage'),
    # path(r'pages/', flatpage, name='django.contrib.flatpages.views.flatpage'),
    # path(r'pages/', include('django.contrib.flatpages.urls')),
    # path(r'ckeditor/', include('ckeditor_uploader.urls')),
    path(r'ckeditor5/', include('django_ckeditor_5.urls')),
    # Language switching
    path(r'i18n/', include('django.conf.urls.i18n')),
    # App-provided paths...
    path(r'admin/', admin.site.urls, name='unfold-admin'),
    # path(r'admin/', unfold_admin_site.urls),  # <-- Unfold admin
    path(r'unfold-admin/', unfold_admin_site.urls),  # <-- Unfold admin
    # Service pages...
    path(
        r'robots.txt',
        cache_page(cache_timeout)(RobotsView.as_view()),
        name='robots',
    ),
    sitemap_url,
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

app_urlpatterns += app_api_urlpatterns

# app_urlpatterns.append(url(r'^translations/', include(translation_urls)))
# app_urlpatterns.append(path(r'^translations/', translation_urls.urlpatterns))

# NOTE: Try to serve a 206 Partial Content for media files on the local dev server (it doesnt (it doesn't work)
# if settings.LOCAL:
#     app_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, view=serve_partial_media)
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
