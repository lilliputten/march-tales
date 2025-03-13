from translated_fields import TranslatedField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model

from tales_django.core.model_helpers import (
    get_non_empty_localized_model_field_attrgetter,
)


class Author(Model):
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    name = TranslatedField(
        models.TextField(_('Name'), blank=False, max_length=256),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    short_description = TranslatedField(
        models.TextField(_('Short description'), blank=True, null=False, max_length=512),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    description = TranslatedField(
        models.TextField(_('Description'), blank=True, null=False, max_length=1024),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    portrait_picture = models.ImageField(_('Portrait picture'), upload_to='authors', blank=True)
    promote = models.BooleanField(_('Promote'), default=False, help_text=_('Promote on the main page'))

    @property
    def tracks_count(self):
        return self.tracks.count()

    def __str__(self):
        return self.name
