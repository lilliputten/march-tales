from datetime import date

from django.db import models
from django.db.models import Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from translated_fields import TranslatedField

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter
from tales_django.entities.Tracks.constants.preview_picture_sizes import (
    author_portrait_picture_full_size,
    author_portrait_picture_jpeg_quality,
    author_portrait_picture_thumb_size,
)

# from datetime import timedelta


# from django.utils.text import slugify


class Author(Model):
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    name = TranslatedField(
        models.CharField(_('Name'), blank=False, max_length=256),
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

    portrait_picture = models.ImageField(_('Portrait picture'), upload_to='authors', blank=False, null=False)
    portrait_picture_full = ImageSpecField(
        source='portrait_picture',
        processors=[
            ResizeToFit(author_portrait_picture_full_size, author_portrait_picture_full_size),
        ],
        format='JPEG',
        options={'quality': author_portrait_picture_jpeg_quality},
    )
    portrait_picture_thumb = ImageSpecField(
        source='portrait_picture',
        processors=[
            ResizeToFit(author_portrait_picture_thumb_size, author_portrait_picture_thumb_size),
        ],
        format='JPEG',
        options={'quality': author_portrait_picture_jpeg_quality},
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

    def get_absolute_url(self):
        # author_name = slugify(self.name)
        return reverse(
            'author_details',
            kwargs={
                'author_id': self.id,
                # 'author_name': author_name,
            },
        )

    def __str__(self):
        return self.name
