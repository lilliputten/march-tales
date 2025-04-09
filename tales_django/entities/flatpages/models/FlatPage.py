from datetime import date

from django.contrib.flatpages.models import FlatPage as BaseFlatPage
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from translated_fields import TranslatedField

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter

# NOTE: For some reason, it doubles the `django_flatpage` db with a `tales_django_flatpage` with doubling fields for `title` and `content`.

# TODO: To investigate it and use only one db or remove doubling fields.

# @see .venv/Lib/site-packages/django/contrib/flatpages/models.py


class FlatPage(BaseFlatPage):
    class Meta:
        db_table = 'tales_django_flatpage'
        verbose_name = _('Flat page')
        verbose_name_plural = _('Flat pages')

    page_title = TranslatedField(
        models.CharField(
            _('Page title'),
            max_length=200,
            default='',
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    page_content = TranslatedField(
        CKEditor5Field(
            _('Page content'),
            blank=True,
            default='',
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    published_at = models.DateField(verbose_name=_('Published at'), default=date.today)
    updated_at = models.DateField(verbose_name=_('Updated at'), auto_now=True)

    def __str__(self):
        items = [
            self.url,
            '—',
            self.page_title,
        ]
        return ' '.join(map(str, filter(None, items)))
