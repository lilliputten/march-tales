from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
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

# Main content URLs with language prefix support via i18n_patterns
# These routes will be accessible with language prefixes like /ru/track/7
i18n_urlpatterns = i18n_patterns(
    # Root page
    path('', index_view, name='index'),
    path('tracks/', index_view, name='tracks'),  # TODO: Create dedicated view in tracks.
    # Secondary & static pages
    # path(r'about/', about_view, name='about'),
    # path(r'about/', RedirectView.as_view(url='/pages/about/', permanent=True)),
    # path(r'application-old/', application_view, name='application'),
    path('terms/', terms_view, name='terms'),
    path('cookies-agreement/', cookies_agreement_view, name='cookies-agreement'),
    path('privacy-policy/', privacy_policy_view, name='privacy-policy'),
    # ckeditor5
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
)

# Flatpages - must be included separately to avoid catch-all <path:url> matching specific routes
# These will be added after specific content patterns in the main urls.py
flatpages_urlpatterns = [
    path('', include('tales_django.entities.flatpages.urls'), name='django.contrib.flatpages.views.flatpage'),
]

# Non-i18n URLs (API, admin, static, services) - no language prefix
app_urlpatterns = [
    # App-provided paths...
    path('admin/', admin.site.urls, name='unfold-admin'),
    # path(r'admin/', unfold_admin_site.urls),  # <-- Unfold admin
    path('unfold-admin/', unfold_admin_site.urls),  # <-- Unfold admin
    # Service pages...
    path(
        'robots.txt',
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
    'i18n_urlpatterns',
    'handler403',
    'handler404',
    'handler500',
]
