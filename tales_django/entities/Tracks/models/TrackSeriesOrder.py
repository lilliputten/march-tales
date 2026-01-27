from django.db import models
from django.utils.translation import gettext_lazy as _

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter


class TrackSeriesOrder(models.Model):
    """
    Intermediate model for the many-to-many relationship between Track and Series,
    allowing us to store the order of tracks within each series.
    """

    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(
        _('Order in Series'),
        default=0,
        help_text=_('Order within the series (lower numbers appear first)'),
    )

    class Meta:
        unique_together = ('series', 'order')  # Ensure unique ordering within each series
        ordering = ['series', 'order']
        indexes = [
            models.Index(fields=['track']),
            models.Index(fields=['series']),
            models.Index(fields=['order']),
            # models.Index(fields=['track', 'series']),
            # models.Index(fields=['series', 'order']),
            # models.Index(fields=['track', 'order']),
            # models.Index(fields=['track', 'order', 'series']),
            # models.Index(fields=['track', 'series', 'order']),
            # models.Index(fields=['series', 'order', 'track']),
            # models.Index(fields=['track', 'series', 'order', 'track']),
            # models.Index(fields=['track', 'series', 'order', 'track', 'series']),
        ]

    def __str__(self):
        return f'{self.track.title} in {self.series.title} (#{self.order})'
