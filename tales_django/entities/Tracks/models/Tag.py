from translated_fields import TranslatedField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter


class Tag(Model):
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    text = TranslatedField(
        models.TextField(
            _('Text'),
            unique=False,
            blank=False,
            null=False,
            max_length=256,
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    promote = models.BooleanField(_('Promote'), default=False, help_text=_('Promote on the main page'))

    @property
    def tracks_count(self):
        return self.track_set.count()

    # Paired (reversed) relation to tracks
    tracks = models.ManyToManyField('Track', blank=True, through='Track_tags')

    def __str__(self):
        return self.text
