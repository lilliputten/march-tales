from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django_registration.forms import RegistrationForm as BaseRegistrationForm

# from ..models import User

# A text field to use in those TextField's which don't require large texts, but can use one-line text inputs
textInputWidget = forms.TextInput(attrs={'class': 'vLargeTextField'})
textAreaWidget = forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 5})


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
