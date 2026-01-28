from django.core.exceptions import ValidationError
from django.forms.models import ModelForm

from tales_django.core.widgets import largeTextAreaWidget, textAreaWidget, textInputWidget

from ..models import Track


class TrackAdminForm(ModelForm):
    class Meta:
        model = Track
        # # NOTE: Don't override crispy forms
        # widgets = {
        #     **{x: textInputWidget for x in Track.title.fields},  # 'title': textInputWidget,
        #     **{x: largeTextAreaWidget for x in Track.description.fields},  # 'description': textAreaWidget,
        #     'youtube_url': textInputWidget,
        #     'audio_file': forms.FileInput(attrs={'accept': '.mp3,audio/*'}),
        # }
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        series = cleaned_data.get('series')
        series_order = cleaned_data.get('series_order')

        if series and series_order is not None:
            # Check if any other track in the same series has the same series_order
            same_order_tracks = Track.objects.filter(series=series, series_order=series_order)

            # If updating an existing track, exclude it from the check
            if self.instance and self.instance.pk:
                same_order_tracks = same_order_tracks.exclude(pk=self.instance.pk)

            if same_order_tracks.exists():
                raise ValidationError(
                    f'Track order {series_order} already exists in series {series.title}. '
                    f'Each track in a series must have a unique order number.'
                )

        return cleaned_data
