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

from ..models import Series


@admin.action(description=_('Promote'))
def promote_action(modeladmin, request, queryset):
    queryset.update(promote=True)


@admin.action(description=_('No promote'))
def no_promote_action(modeladmin, request, queryset):
    queryset.update(promote=False)


@admin.register(Series, site=unfold_admin_site)
class SeriesAdmin(TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    actions = [
        promote_action,
        no_promote_action,
    ]
    list_display = [
        'title_translated',
        'serialized_tracks_count',
        'promote',
        'is_visible',
        # 'created_at',
        'updated_at',
    ]
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    search_fields = [
        'title_en',
        'title_ru',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _tracks_count=Count('tracks', distinct=True),
            _title_translated=F('title_' + get_language()),
        )
        return queryset

    def title_translated(self, track):
        return track.title

    title_translated.admin_order_field = Lower('_title_translated')
    title_translated.short_description = _('title')

    def serialized_tracks_count(self, obj):
        return obj._tracks_count

    serialized_tracks_count.admin_order_field = '_tracks_count'
    serialized_tracks_count.short_description = _('tracks count')

    def get_ordering(self, request):
        return [Lower(to_attribute('title'))]
