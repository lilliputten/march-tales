from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm

# from ..models import User

# A text field to use in those TextField's which don't require large texts, but can use one-line text inputs
textInputWidget = forms.TextInput(attrs={'class': 'vLargeTextField'})
textAreaWidget = forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 5})
