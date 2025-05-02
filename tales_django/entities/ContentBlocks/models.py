from datetime import date

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from translated_fields import TranslatedField

from tales_django.core.helpers import remove_html_tags
from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter, localized_field_name


class ContentBlocks(models.Model):
    STRING = 'STRING'
    BLOCK = 'BLOCK'
    RICH_BLOCK = 'RICH_BLOCK'
    TYPE = [
        (STRING, _('String')),
        (BLOCK, _('Block')),
        (RICH_BLOCK, _('Rich block')),
    ]
    type = models.CharField(_('Type'), choices=TYPE, max_length=16, blank=False, default=STRING)

    name = models.CharField(_('Name'), max_length=100)
    content = TranslatedField(
        CKEditor5Field(
            _('Content'),
            blank=True,
            default='',
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    created_at = models.DateField(verbose_name=_('Created at'), default=date.today)
    updated_at = models.DateField(verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('content block')
        verbose_name_plural = _('content blocks')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        type = self.type
        if type != ContentBlocks.RICH_BLOCK:
            for lang in settings.LANGUAGES_LIST:
                field = localized_field_name('content', lang)
                val = getattr(self, field)
                val = remove_html_tags(val)
                setattr(self, field, val)
        super(ContentBlocks, self).save(*args, **kwargs)
