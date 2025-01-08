from translated_fields import TranslatedField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model


class Author(Model):
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    name = TranslatedField(models.TextField(_('name'), blank=False, max_length=150))
    description = TranslatedField(models.TextField(_('description'), blank=True, null=False, max_length=512))
    portrait_picture = models.ImageField(_('portrait picture'), upload_to='authors', blank=True)
    promote = models.BooleanField(_('promote'), default=False, help_text=_('Promote on the main page'))

    def __str__(self):
        return self.name
