from django import forms
from django.contrib import admin
from django.db.models import F
from django.db.models.functions import Lower
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedFieldAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.sites import unfold_admin_site

from ..models import Series, Track
from ..models.TrackSeriesOrder import TrackSeriesOrder


class TrackSeriesOrderInline(admin.TabularInline):
    model = TrackSeriesOrder
    fk_name = 'series'
    extra = 1
    max_num = 100
    fields = ('track', 'order')
    verbose_name = _('Track in Series')
    verbose_name_plural = _('Tracks in this Series')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'track':
            # Filter out tracks already associated with this series
            if hasattr(self, 'parent_obj') and self.parent_obj:
                existing_track_ids = TrackSeriesOrder.objects.filter(series=self.parent_obj).values_list(
                    'track_id', flat=True
                )
                kwargs['queryset'] = Track.objects.exclude(id__in=existing_track_ids)
            else:
                kwargs['queryset'] = Track.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Series, site=unfold_admin_site)
class SeriesAdmin(TranslatedFieldAdmin, UnfoldModelAdmin):
    inlines = [TrackSeriesOrderInline]

    fieldsets = (
        (
            _('Title'),
            {
                'classes': ['--collapse', '--opened-by-default', 'columns'],
                'fields': (
                    'title_ru',
                    'title_en',
                ),
            },
        ),
        (
            _('Description'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'description_ru',
                    'description_en',
                ),
            },
        ),
        (
            _('Settings'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': ('is_visible',),
            },
        ),
    )

    list_display = [
        'title_translated',
        'track_count',
        'published_track_count',
        'is_visible',
        'created_at',
        'updated_at',
    ]

    list_filter = [
        'is_visible',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'title_en',
        'title_ru',
        'description_en',
        'description_ru',
    ]

    readonly_fields = (
        'track_count',
        'published_track_count',
        'created_at',
        'updated_at',
    )

    def track_count(self, series):
        # Import here to avoid circular imports
        from ..models import Series as SeriesModel

        if isinstance(series, SeriesModel):
            return series.track_count
        return 0

    track_count.short_description = _('Total Tracks')

    def published_track_count(self, series):
        # Import here to avoid circular imports
        from ..models import Series as SeriesModel

        if isinstance(series, SeriesModel):
            return series.published_track_count
        return 0

    published_track_count.short_description = _('Published Tracks')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _title_translated=F('title_' + get_language()),
        )
        return queryset

    def title_translated(self, series):
        return series.title

    title_translated.admin_order_field = Lower('_title_translated')
    title_translated.short_description = _('Title')
