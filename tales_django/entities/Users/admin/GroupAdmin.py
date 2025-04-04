from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib import admin

# from translated_fields import TranslatedFieldAdmin

from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from translated_fields import TranslatedFieldAdmin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.sites import unfold_admin_site


class Group(BaseGroup):
    """Instead of trying to get new user under existing `Aunthentication and Authorization`
    banner, create a proxy group model under our Accounts app label.
    Refer to: https://github.com/tmm/django-username-email/blob/master/cuser/admin.py
    """

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        proxy = True


admin.site.unregister(BaseGroup)


# @admin.register(Group)
# class GroupAdmin(BaseGroupAdmin):
@admin.register(Group, site=unfold_admin_site)
class GroupAdmin(
    BaseGroupAdmin, TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin
):
    import_form_class = ImportForm
    export_form_class = ExportForm
    # pass
