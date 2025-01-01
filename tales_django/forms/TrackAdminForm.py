from django.contrib.auth import get_user_model
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
        }
        fields = '__all__'
