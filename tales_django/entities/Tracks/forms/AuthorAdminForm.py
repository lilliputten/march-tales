from django.forms.models import ModelForm

from tales_django.core.widgets import textInputWidget, textAreaWidget

from ..models import Author


class AuthorAdminForm(ModelForm):
    class Meta:
        model = Author
        widgets = {
            # 'name': textInputWidget,
            **{x: textInputWidget for x in Author.name.fields},  # 'name': textInputWidget,
            **{x: textAreaWidget for x in Author.description.fields},  # 'description': textInputWidget,
        }
        fields = '__all__'
