from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from ..models import Track
from ..forms import TrackAdminForm


class IsPublishedFilter(SimpleListFilter):
    """
    Published tracks filter
    """

    title = 'Published'
    parameter_name = 'is_published'

    def lookups(self, _, __):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, _, queryset):
        if self.value() == '1':
            return queryset.filter(track_status='PUBLISHED')
        if self.value() == '0':
            return queryset.filter(~Q(track_status='PUBLISHED'))


class TrackAdmin(admin.ModelAdmin):
    form = TrackAdminForm
    list_display = [
        'title',
        'created_by',
        'created_at',
        'is_published',
    ]
    exclude = (
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    )
    list_filter = [
        IsPublishedFilter,
    ]

    def is_published(self, user):
        return user.track_status == 'PUBLISHED'

    is_published.short_description = 'Published'
    is_published.boolean = True

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):
        """
        Auto update owning users
        """
        if not obj.created_by_id:
            obj.created_by_id = request.user.id
        obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)


admin.site.register(Track, TrackAdmin)
