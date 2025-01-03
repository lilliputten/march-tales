from django.forms.models import ModelForm

from tales_django.core.widgets import textInputWidget

from ..models import Author


class AuthorAdminForm(ModelForm):
    class Meta:
        model = Author
        widgets = {
            'name': textInputWidget,
        }
        fields = '__all__'
