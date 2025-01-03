from django.contrib import admin
from django.db.models import Count

from ..models import Tag
from ..forms import TagAdminForm


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = [
        'text',
        'promote',
        'tagged_tracks_count',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _tracks_count=Count('tracks', distinct=True),
        )
        return queryset

    def tagged_tracks_count(self, obj):
        return obj._tracks_count

    tagged_tracks_count.admin_order_field = '_tracks_count'
