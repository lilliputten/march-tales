from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.sites import unfold_admin_site


@admin.register(Site, site=unfold_admin_site)
class SiteAdmin(BaseSiteAdmin, UnfoldModelAdmin):
    pass
