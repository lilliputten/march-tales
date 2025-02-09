from translated_fields import TranslatedField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter


class Rubric(Model):
    class Meta:
        verbose_name = _('rubric')
        verbose_name_plural = _('rubrics')

    text = TranslatedField(
        models.TextField(
            _('text'),
            unique=False,
            blank=False,
            null=False,
            max_length=150,
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    promote = models.BooleanField(_('promote'), default=False, help_text=_('Promote on the main page'))

    @property
    def tracks_count(self):
        return self.tracks.count()

    # Paired (reversed) relation to tracks
    tracks = models.ManyToManyField('Track', blank=True, through='Track_rubrics')

    def __str__(self):
        return self.text
