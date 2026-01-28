from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Track


class TrackInlineForm(admin.TabularInline):
    """
    Inline admin for managing tracks directly from the Series admin page.
    """

    model = Track
    fk_name = 'series'  # Specify which foreign key to use
    extra = 1  # Number of empty forms to display
    fields = ('title_ru', 'title_en', 'series_order')
    verbose_name = _('Track')
    verbose_name_plural = _('Tracks')
