from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from ..forms import UserAdminForm
from ..models import User


class IsRegularUserFilter(SimpleListFilter):
    """
    Regular user custom combined filter
    """

    title = 'Is regular user'
    parameter_name = 'is_regular_user'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, _request, queryset):
        if self.value() == '1':
            return queryset.filter(is_staff=False, is_superuser=False)
        if self.value() == '0':
            return queryset.filter(~Q(is_staff=False, is_superuser=False))


class UserAdmin(BaseUserAdmin):
    form = UserAdminForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'address')}),
        (
            'Tracks',
            {
                'fields': (
                    'favorite_tracks',
                    'playlist_tracks',
                )
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    # 'groups',
                    # 'user_permissions',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_regular_user',
    ]
    list_filter = [
        IsRegularUserFilter,
    ]

    def is_regular_user(self, user):
        return not user.is_staff and not user.is_superuser

    is_regular_user.short_description = 'Regular user'
    is_regular_user.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['username'].label = 'Email (username)'
        return form


admin.site.register(User, UserAdmin)
