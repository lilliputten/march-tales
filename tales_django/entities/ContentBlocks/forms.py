from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContentBlocks


class ContentBlocksForm(forms.ModelForm):
    class Meta:
        model = ContentBlocks
        fields = '__all__'
        # exclude = ['type']
