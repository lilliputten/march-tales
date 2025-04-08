from django.contrib.flatpages.forms import FlatpageForm as BaseFlatpageForm
from django.contrib.flatpages.models import FlatPage as BaseFlatPage
from django.utils.translation import gettext_lazy as _

from ..models import FlatPage


class FlatPageForm(BaseFlatpageForm):
    class Meta:
        model = FlatPage
        fields = '__all__'
        exclude = ['title', 'content']
