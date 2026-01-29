from django.contrib import admin
from django.db.models import Count, F
from django.db.models.functions import Lower
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from translated_fields import TranslatedFieldAdmin, to_attribute
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from tales_django.sites import unfold_admin_site

from ..models import Rubric


@admin.action(description=_('Promote'))
def promote_action(modeladmin, request, queryset):
    queryset.update(promote=True)


@admin.action(description=_('No promote'))
def no_promote_action(modeladmin, request, queryset):
    queryset.update(promote=False)


@admin.register(Rubric, site=unfold_admin_site)
class RubricAdmin(TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        (
            _('Text'),
            {
                'classes': ['--collapse', '--opened-by-default', 'columns'],
                'fields': (
                    'text_ru',
                    'text_en',
                ),
            },
        ),
        (
            _('Properties'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'tracks',
                    'promote',
                ),
            },
        ),
        (
            _('Updates'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'published_at',
                    'updated_at',
                ),
            },
        ),
    )

    actions = [
        promote_action,
        no_promote_action,
    ]
    list_display = [
        'text_translated',
        'rubricated_tracks_count',
        'promote',
        # 'published_at',
        'updated_at',
    ]
    readonly_fields = (
        'published_at',
        'updated_at',
    )
    search_fields = [
        'text_en',
        'text_ru',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _tracks_count=Count('tracks', distinct=True),
            _text_translated=F('text_' + get_language()),
        )
        return queryset

    def text_translated(self, track):
        return track.text

    text_translated.admin_order_field = Lower('_text_translated')
    text_translated.short_description = _('text')

    def rubricated_tracks_count(self, obj):
        return obj._tracks_count

    rubricated_tracks_count.admin_order_field = '_tracks_count'
    rubricated_tracks_count.short_description = _('tracks count')

    def get_ordering(self, request):
        return [Lower(to_attribute('text'))]
