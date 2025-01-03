from django.forms.models import ModelForm

from tales_django.core.widgets import textInputWidget

from ..models import Tag


class TagAdminForm(ModelForm):
    class Meta:
        model = Tag
        widgets = {
            'text': textInputWidget,
        }
        fields = '__all__'
