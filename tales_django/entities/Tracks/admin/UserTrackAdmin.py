from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from translated_fields import TranslatedFieldAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from tales_django.sites import unfold_admin_site

from ..models import UserTrack


@admin.register(UserTrack, site=unfold_admin_site)
class UserTrackAdmin(
    TranslatedFieldAdmin,
    ImportExportModelAdmin,
    ExportActionModelAdmin,
    UnfoldModelAdmin,
):
    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        (
            _('Basic'),
            {
                'classes': ['columns'],
                'fields': (
                    'user',
                    'track',
                ),
            },
        ),
        (
            _('Favorite'),
            {
                'classes': ['columns'],
                'fields': (
                    'is_favorite',
                    'favorited_at',
                ),
            },
        ),
        (
            _('Playback'),
            {
                'classes': ['columns'],
                'fields': (
                    'played_count',
                    'position',
                    'played_at',
                ),
            },
        ),
        (
            _('Information'),
            {
                'classes': ['columns'],
                'fields': ('updated_at',),
            },
        ),
    )

    list_display = [
        'track',
        'user',
        'is_favorite',
        'favorited_at',
        'played_count',
        'position_formatted',
        'played_at',
        'updated_at',
    ]
    readonly_fields = ('updated_at',)
    search_fields = [
        'track__title_ru',
        'track__title_en',
        'user__email',
    ]
    list_filter = [
        'is_favorite',
        # 'position',
        'favorited_at',
        'played_at',
        'updated_at',
        'played_count',
        'track',
        'user',
    ]

    def position_formatted(self, track):
        return track.position_formatted

    position_formatted.admin_order_field = 'position'

    position_formatted.short_description = _('Position')
