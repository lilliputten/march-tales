from django import forms
from django.forms.models import ModelForm

from ..models import Track

from .common_widgets import textAreaWidget, textInputWidget


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

    # def form_valid(self, form):
    #     files = form.cleaned_data['audio_file']
    #     # for f in files:
    #     #     ...  # Do something with each file.
    #     return super().form_valid(form)
