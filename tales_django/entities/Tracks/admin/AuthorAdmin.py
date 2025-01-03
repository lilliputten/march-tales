from django.contrib import admin
from django.db.models import Count

from ..models import Author
from ..forms import AuthorAdminForm


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    list_display = [
        'name',
        'promote',
        # 'track_count',
        'has_portrait',
    ]

    def has_portrait(self, track):
        return True if track.portrait_picture else False

    has_portrait.admin_order_field = 'portrait_picture'

    has_portrait.short_description = 'Has portrait'
    has_portrait.boolean = True

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         _tracks_count=Count('tracks', distinct=True),
    #     )
    #     return queryset
    #
    # def track_count(self, obj):
    #     return obj._tracks_count
    #
    # track_count.admin_order_field = '_tracks_count'
