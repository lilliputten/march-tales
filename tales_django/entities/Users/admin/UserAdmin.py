from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from translated_fields import TranslatedFieldAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from tales_django.sites import unfold_admin_site

from ..models import User


class IsAdministratorFilter(admin.SimpleListFilter):
    """
    Regular user custom combined filter
    """

    title = _('Is administrator')
    parameter_name = 'is_administrator'

    def lookups(self, request, model_admin):
        return (
            ('1', _('True')),
            ('0', _('False')),
        )

    def queryset(self, _request, queryset):
        if self.value() == '1':
            return queryset.filter(~Q(is_staff=False, is_superuser=False))
        if self.value() == '0':
            return queryset.filter(is_staff=False, is_superuser=False)


@admin.register(User, site=unfold_admin_site)
class UserAdmin(BaseUserAdmin, TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    # 'address',
                )
            },
        ),
        (
            _('Tracks'),
            {
                'fields': (
                    'favorite_tracks',
                    # 'playlist_tracks',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'allow_notifications',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    # 'groups',
                    # 'user_permissions',
                )
            },
        ),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_administrator',
        'allow_notifications',
    ]
    search_fields = [
        'email',
        'first_name',
        'last_name',
    ]
    list_filter = [
        IsAdministratorFilter,
        'allow_notifications',
        # 'is_administrator',
    ]

    def is_administrator(self, user):
        return user.is_staff or user.is_superuser

    def is_regular_user(self, user):
        return not user.is_staff and not user.is_superuser

    is_administrator.short_description = _('Administrator')
    is_administrator.boolean = True
    is_administrator.admin_order_field = 'is_staff'

    is_regular_user.short_description = _('Regular user')
    is_regular_user.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['username'].label = _('E-mail (username)')
        # form.base_fields['address'].label = _('Address')
        return form
