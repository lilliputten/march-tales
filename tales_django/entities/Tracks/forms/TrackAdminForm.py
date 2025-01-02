from django.forms.models import ModelForm

from tales_django.core.widgets import textAreaWidget, textInputWidget

from ..models import Track


class TrackAdminForm(ModelForm):
    class Meta:
        model = Track
        widgets = {
            'title': textInputWidget,
            'youtube_url': textInputWidget,
            'description': textAreaWidget,
            'tags_list': textAreaWidget,
            # 'audio_file': forms.FileInput(attrs={'accept': '.mp3,audio/*'}),
        }
        fields = '__all__'
