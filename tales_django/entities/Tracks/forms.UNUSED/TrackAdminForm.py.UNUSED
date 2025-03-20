# from translated_fields import TranslatedFieldAdmin
from django.forms.models import ModelForm

from tales_django.core.widgets import textAreaWidget, textInputWidget, largeTextAreaWidget

from ..models import Track


class TrackAdminForm(ModelForm):
    class Meta:
        model = Track
        widgets = {
            **{x: textInputWidget for x in Track.title.fields},  # 'title': textInputWidget,
            **{x: largeTextAreaWidget for x in Track.description.fields},  # 'description': textAreaWidget,
            'youtube_url': textInputWidget,
            # 'audio_file': forms.FileInput(attrs={'accept': '.mp3,audio/*'}),
        }
        fields = '__all__'
