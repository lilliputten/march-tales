from django.forms.models import ModelForm

from tales_django.core.widgets import textInputWidget

from ..models import Rubric


class RubricAdminForm(ModelForm):
    class Meta:
        model = Rubric
        widgets = {
            'text': textInputWidget,
        }
        fields = '__all__'
