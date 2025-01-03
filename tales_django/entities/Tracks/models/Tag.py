# from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models import Model


class Tag(Model):
    text = models.TextField(
        unique=False,
        blank=False,
        null=False,
        max_length=150,
    )

    promote = models.BooleanField(default=False, verbose_name='Promote on the main page')

    @property
    def tracks_count(self):
        return self.track_set.count()

    # Paired rback relation to tracks
    tracks = models.ManyToManyField('Track', blank=True, through='Track_tags')

    def __str__(self):
        return self.text
