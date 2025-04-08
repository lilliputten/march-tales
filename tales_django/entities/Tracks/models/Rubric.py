from datetime import date

from django.db import models
from django.db.models import Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter


class Rubric(Model):
    class Meta:
        verbose_name = _('Rubric')
        verbose_name_plural = _('Rubrics')

    text = TranslatedField(
        models.CharField(
            _('Text'),
            unique=False,
            blank=False,
            null=False,
            max_length=256,
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    promote = models.BooleanField(_('Promote'), default=True, help_text=_('Promote on the main page'))

    published_at = models.DateField(verbose_name=_('Published at'), default=date.today)
    updated_at = models.DateField(verbose_name=_('Updated at'), auto_now=True)

    @property
    def tracks_count(self):
        return self.tracks.count()

    @property
    def published_tracks_count(self):
        return self.tracks.filter(track_status='PUBLISHED').count()

    # Paired (reversed) relation to tracks
    tracks = models.ManyToManyField('Track', blank=True, through='Track_rubrics')

    def get_absolute_url(self):
        return reverse(
            'rubric_details',
            kwargs={
                'rubric_id': self.id,
            },
        )

    def __str__(self):
        return self.text
