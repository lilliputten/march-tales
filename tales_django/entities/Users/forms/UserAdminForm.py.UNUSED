from django.contrib.auth import get_user_model
from django.forms.models import ModelForm

from tales_django.core.widgets import textAreaWidget, textInputWidget


class UserAdminForm(ModelForm):
    class Meta:
        # model = User
        model = get_user_model()
        widgets = {
            'first_name': textInputWidget,
            'last_name': textInputWidget,
            'address': textAreaWidget,
        }
        fields = '__all__'
