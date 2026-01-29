from django import forms
from django.contrib import admin, messages
from django.db.models import Count, F
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from translated_fields import TranslatedFieldAdmin, to_attribute
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from tales_django.sites import unfold_admin_site

from ..forms.TrackInlineForm import TrackInlineAdmin
from ..models import Series, Track
from .views.update_series_tracks import update_series_tracks


@admin.action(description=_('Promote'))
def promote_action(modeladmin, request, queryset):
    queryset.update(promote=True)


@admin.action(description=_('No promote'))
def no_promote_action(modeladmin, request, queryset):
    queryset.update(promote=False)


class TrackAssignmentForm(forms.Form):
    """
    Form to select an existing track to assign to a series.
    """

    select_track = forms.ModelChoiceField(
        queryset=Track.objects.none(),
        required=False,
        empty_label=_('Select a track to add'),
        label=_('Select track to add to this series'),
        widget=forms.Select(attrs={'class': 'select2'}),
    )

    def __init__(self, *args, **kwargs):
        series_instance = kwargs.pop('series_instance', None)
        super().__init__(*args, **kwargs)

        if series_instance:
            # Get tracks that are not already in this series
            # tracks_already_in_series = series_instance.tracks.values_list('id', flat=True)
            available_tracks = Track.objects   # .exclude(id__in=tracks_already_in_series)
            self.fields['select_track'].queryset = available_tracks


@admin.register(Series, site=unfold_admin_site)
class SeriesAdmin(TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin):
    inlines = [TrackInlineAdmin]
    import_form_class = ImportForm
    export_form_class = ExportForm
    # change_form_template = 'admin/entities/Tracks/series/change_form.html'
    change_form_template = 'overriden/admin/Series/change_form.html'

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
            _('Status'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'promote',
                    'is_visible',
                ),
            },
        ),
        (
            _('Updates'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'created_at',
                    'updated_at',
                ),
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:series_id>/update-tracks/',
                self.admin_site.admin_view(update_series_tracks),
                name='update_series_tracks',
            ),
        ]
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        series = self.get_object(request, object_id)

        if request.method == 'POST' and 'select_track' in request.POST:
            # Handle track assignment form submission
            track_assignment_form = TrackAssignmentForm(request.POST, series_instance=series)
            if track_assignment_form.is_valid():
                selected_track = track_assignment_form.cleaned_data['select_track']
                if selected_track:
                    selected_track.series = series
                    selected_track.series_order = series.tracks.count() + 1
                    selected_track.save()
                    messages.success(
                        request, _('Track "%(track)s" has been added to the series.') % {'track': selected_track.title}
                    )
                # Redirect to refresh the page after assignment
                return HttpResponseRedirect(request.path)
        else:
            # Display the form for GET requests or after successful assignment
            track_assignment_form = TrackAssignmentForm(series_instance=series)

        if series:
            # Add form to select existing tracks to assign
            extra_context['track_assignment_form'] = track_assignment_form
            # For now, we'll handle the assignment via a POST to the same page
            extra_context['assign_tracks_url'] = request.path

        return super().change_view(request, object_id, form_url, extra_context)

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
