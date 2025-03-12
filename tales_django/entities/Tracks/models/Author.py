from translated_fields import TranslatedField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model

from tales_django.core.model_helpers import (
    get_non_empty_localized_model_field_attrgetter,
)


class Author(Model):
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    name = TranslatedField(
        models.TextField(_('name'), blank=False, max_length=150),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    short_description = TranslatedField(
        models.TextField(_('short description'), blank=True, null=False, max_length=512),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    description = TranslatedField(
        models.TextField(_('description'), blank=True, null=False, max_length=4096),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    portrait_picture = models.ImageField(_('portrait picture'), upload_to='authors', blank=True)
    promote = models.BooleanField(_('promote'), default=False, help_text=_('Promote on the main page'))

    @property
    def tracks_count(self):
        return self.tracks.count()

    def __str__(self):
        return self.name
