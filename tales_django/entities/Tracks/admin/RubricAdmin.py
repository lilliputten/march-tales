from django.contrib import admin
from django.db.models import Count

from ..models import Rubric
from ..forms import RubricAdminForm


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    form = RubricAdminForm
    list_display = [
        'text',
        'promote',
        'rubricated_tracks_count',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _tracks_count=Count('tracks', distinct=True),
        )
        return queryset

    def rubricated_tracks_count(self, obj):
        return obj._tracks_count

    rubricated_tracks_count.admin_order_field = '_tracks_count'
