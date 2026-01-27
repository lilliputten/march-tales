from django.db import models
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter

from .TrackSeriesOrder import TrackSeriesOrder


class Series(models.Model):
    class Meta:
        verbose_name = _('Series')
        verbose_name_plural = _('Series')
        # indexes = [
        #     models.Index(fields=['title_ru']),
        #     models.Index(fields=['title_en']),
        #     models.Index(fields=['created_at']),
        # ]

    title = TranslatedField(
        models.CharField(
            _('Title'),
            unique=False,
            blank=False,
            null=False,
            max_length=256,
            help_text=_('The series title text, required.'),
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    description = TranslatedField(
        models.TextField(
            _('Description'),
            blank=True,
            null=False,
            max_length=1024,
            help_text=_('Optional series description'),
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    is_visible = models.BooleanField(
        _('Visible'),
        default=True,
        help_text=_('Whether this series is visible to users'),
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
    )

    tracks = models.ManyToManyField(
        'Track',
        through='TrackSeriesOrder',
        related_name='series',
        verbose_name=_('Tracks'),
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Link to the first track in the series ordered by track order
        first_track_order = (
            TrackSeriesOrder.objects.filter(series=self, track__track_status='PUBLISHED')
            .order_by('series_order')
            .first()
        )

        if first_track_order:
            return first_track_order.track.get_absolute_url()
        return '#'

    @property
    def track_count(self):
        from .TrackSeriesOrder import TrackSeriesOrder

        return TrackSeriesOrder.objects.filter(series=self).count()

    @property
    def published_track_count(self):
        from .TrackSeriesOrder import TrackSeriesOrder

        return TrackSeriesOrder.objects.filter(series=self, track__track_status='PUBLISHED').count()
