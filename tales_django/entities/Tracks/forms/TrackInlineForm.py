from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from ..models import Series, Track


class TrackAssignmentForm(forms.Form):
    """
    Form to select existing tracks to assign to a series.
    """

    tracks_to_add = forms.ModelMultipleChoiceField(
        queryset=Track.objects.none(),  # Will be populated dynamically
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Select tracks to add to this series'),
    )

    def __init__(self, *args, **kwargs):
        series_instance = kwargs.pop('series_instance', None)
        super().__init__(*args, **kwargs)

        if series_instance:
            # Get tracks that are not already in this series
            tracks_already_in_series = series_instance.tracks.values_list('id', flat=True)
            available_tracks = Track.objects.exclude(id__in=tracks_already_in_series)
            self.fields['tracks_to_add'].queryset = available_tracks


# class TrackSelectorWidget(forms.Select):
#     """
#     Custom widget to select existing tracks that are not already in the series.
#     """
#
#     def __init__(self, series_instance=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.series_instance = series_instance
#
#     def build_attrs(self, base_attrs, extra_attrs=None):
#         attrs = super().build_attrs(base_attrs, extra_attrs)
#         # Add data attributes that can be used by JavaScript
#         if self.series_instance:
#             attrs['data-series-id'] = self.series_instance.id
#         attrs['class'] = attrs.get('class', '') + ' track-selector-dropdown'
#         return attrs


# class TrackSelectorForm(forms.Form):
#     """
#     Form with a dropdown to select existing tracks to add to the series.
#     """
#
#     select_track = forms.ModelChoiceField(
#         queryset=Track.objects.none(),
#         required=False,
#         empty_label=_('Select a track to add'),
#         label=_('Add existing track to series'),
#         widget=TrackSelectorWidget(),
#     )
#
#     def __init__(self, *args, **kwargs):
#         series_instance = kwargs.pop('series_instance', None)
#         super().__init__(*args, **kwargs)
#
#         if series_instance:
#             # Get tracks that are not already in this series
#             tracks_already_in_series = series_instance.tracks.values_list('id', flat=True)
#             available_tracks = Track.objects.exclude(id__in=tracks_already_in_series)
#             self.fields['select_track'].queryset = available_tracks
#             # Update the widget with the series instance
#             self.fields['select_track'].widget.series_instance = series_instance


# class TrackSelectionForm(forms.Form):
#     """Selection-only form for existing tracks"""
#
#     track_id = forms.ModelChoiceField(
#         queryset=Track.objects.none(),
#         label=_('Select track to add'),
#         empty_label=_('Choose a track...'),
#         widget=forms.Select(attrs={'class': 'select2'}),
#     )


class TrackInlineForm(admin.TabularInline):
    """
    Inline admin for managing tracks directly from the Series admin page.

    @see Added form complement to add new tracks:

    - tales_django/templates/admin/entities/Tracks/series/change_form.html

    @see Form customization in:

    - static/unfold-fixes/unfold-fixes.css
    - static/unfold-fixes/unfold-fixes.js

    @see Installed unfold styles:

    - .venv/Lib/site-packages/unfold/static/unfold/css

    """

    model = Track
    fk_name = 'series'  # Specify which foreign key to use
    extra = 0  # No empty forms to prevent creating new tracks directly
    can_add = False  # Disable the add button
    fields = (
        'id',
        # 'title_ru',
        # 'title_en',
        'series_order',
    )
    verbose_name = _('Track')
    verbose_name_plural = _('Tracks')
    can_delete = True  # Allow removal of existing tracks from the series
    show_change_link = False  # Don't show change link since we're not editing data
    # readonly_fields = ('title_ru', 'title_en', 'series_order')  # Make fields read-only to prevent editing
