from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model


class Rubric(Model):
    class Meta:
        verbose_name = _('rubric')
        verbose_name_plural = _('rubrics')

    text = models.TextField(
        unique=False,
        blank=False,
        null=False,
        max_length=150,
    )

    promote = models.BooleanField(default=False, help_text=_('Promote on the main page'))

    @property
    def tracks_count(self):
        return self.track_set.count()

    # Paired (reversed) relation to tracks
    tracks = models.ManyToManyField('Track', blank=True, through='Track_rubrics')

    def __str__(self):
        return self.text
