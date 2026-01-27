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


class TrackInlineForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = '__all__'
        widgets = {
            'series_order': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter order number'),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent styling to the series_order field
        self.fields['series_order'].widget.attrs.update(
            {
                'class':  ' '.join([
                    'border',
                    'border-base-200',
                    'bg-white',
                    'font-medium',
                    'min-w-20',
                    'placeholder-base-400',
                    'rounded',
                    'shadow-sm',
                    'text-font-default-light',
                    'text-sm',
                    'focus:ring',
                    'focus:ring-primary-300',
                    'focus:border-primary-600',
                    'focus:outline-none',
                    'group-[.errors]:border-red-600',
                    'group-[.errors]:focus:ring-red-200',
                    'dark:bg-base-900',
                    'dark:border-base-700',
                    'dark:text-font-default-dark',
                    'dark:focus:border-primary-600',
                    'dark:focus:ring-primary-700',
                    'dark:focus:ring-opacity-50',
                    'dark:group-[.errors]:border-red-500',
                    'dark:group-[.errors]:focus:ring-red-600/40',
                    'px-3',
                    'py-2',
                    'max-w-full',
                    # 'max-w-2xl'
                ]),
            }
        )


class TrackInline(admin.TabularInline):
    model = Track
    form = TrackInlineForm
    fk_name = 'series'
    extra = 0
    fields = ('title_display', 'series_order')
    readonly_fields = ('title_display',)
    verbose_name = _('Track in Series')
    verbose_name_plural = _('Tracks in this Series')

    def title_display(self, obj):
        if obj.title:
            # Show translated title based on current language
            lang_title = getattr(obj, f'title_{get_language()[:2]}', None)
            return lang_title or str(obj.title)
        return '- No Title -'

    title_display.short_description = _('Track Title')


@admin.register(Series, site=unfold_admin_site)
class SeriesAdmin(TranslatedFieldAdmin, UnfoldModelAdmin):
    inlines = [TrackInline]

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
