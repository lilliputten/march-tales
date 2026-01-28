from datetime import date

from django.db import models
from django.db.models import Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter


class Series(Model):
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

    promote = models.BooleanField(_('Promote'), default=True, help_text=_('Promote on the main page'))

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

    @property
    def tracks_count(self):
        return self.tracks.count()

    @property
    def published_tracks_count(self):
        return self.tracks.filter(track_status='PUBLISHED').count()

    # The tracks relationship is now handled by the ForeignKey on the Track model
    # Access tracks via the related_name 'tracks' from Track.series

    # def get_absolute_url(self):
    #     return reverse(
    #         'series_details',
    #         kwargs={
    #             'series_id': self.id,
    #         },
    #     )

    def __str__(self):
        return self.title
