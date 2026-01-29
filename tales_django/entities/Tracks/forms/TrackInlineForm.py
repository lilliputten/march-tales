from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Series, Track

# from .TrackInlineFormSet import TrackInlineFormSet


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
            # tracks_already_in_series = series_instance.tracks.values_list('id', flat=True)
            available_tracks = Track.objects.all()   # exclude(id__in=tracks_already_in_series)
            self.fields['tracks_to_add'].queryset = available_tracks


class TrackInlineForm(forms.ModelForm):
    """
    Form for individual track in the inline formset.
    This form excludes validation for fields that are not meant to be edited in the Series admin.
    """

    class Meta:
        model = Track
        fields = (
            'id',  # Track ID (primary key)
            'series_order',  # Order within series
        )
        widgets = {
            'id': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make ID read-only
        if 'id' in self.fields:
            self.fields['id'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        # Ensure the series is properly set before saving
        # The series should be set by the formset, but let's ensure it here too
        return super().save(commit=commit)


class TrackInlineAdmin(admin.TabularInline):
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
    form = TrackInlineForm  # Use the custom form
    # formset = TrackInlineFormSet  # Use custom formset
    fk_name = 'series'  # Specify which foreign key to use
    extra = 0  # No empty forms to prevent creating new tracks directly
    can_add = False  # Disable the add button
    fields = (
        'id',  # Track ID (primary key)
        'series_order',  # Order within series
    )
    verbose_name = _('Track')
    verbose_name_plural = _('Tracks')
    can_delete = True  # Allow removal of existing tracks from the series
    show_change_link = False  # Don't show change link since we're not editing data
    # readonly_fields = ('id',)  # Make ID read-only
