from django.db import models
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter


class Series(models.Model):
    class Meta:
        verbose_name = _('Series')
        verbose_name_plural = _('Series')

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Link to the first track in the series
        first_track = self.tracks.filter(track_status='PUBLISHED').first()
        if first_track:
            return first_track.get_absolute_url()
        return '#'

    @property
    def track_count(self):
        return self.tracks.count()

    @property
    def published_track_count(self):
        return self.tracks.filter(track_status='PUBLISHED').count()
