from datetime import date, timedelta

from django.db import models
from django.db.models import Model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from translated_fields import TranslatedField

from core.appEnv import LOCAL
from core.helpers.files import sizeofFmt
from core.logging import getDebugLogger
from tales_django.core.helpers.audio import getAudioTrackFolderName
from tales_django.core.model_helpers import \
    get_non_empty_localized_model_field_attrgetter
from tales_django.entities.Tracks.constants.preview_picture_sizes import (
    track_preview_picture_full_size, track_preview_picture_jpeg_quality,
    track_preview_picture_thumb_size)

_logger = getDebugLogger()


class Track(Model):
    class Meta:
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')

    title = TranslatedField(
        models.CharField(
            _('Title'),
            unique=False,
            blank=False,
            null=False,
            max_length=256,
            # verbose_name='track title',
            help_text=_('The track title text, required.'),
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    description = TranslatedField(
        models.TextField(
            _('Description'),
            blank=True,
            null=False,
            max_length=1024,
            help_text=_('Optional description'),
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    youtube_url = models.URLField(
        verbose_name=_('Youtube link'),
        blank=True,
        null=False,
        max_length=64,
        help_text=_('YouTube video link url'),
    )

    author = models.ForeignKey(
        'Author',
        verbose_name=_('Author'),
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
    )

    tags = models.ManyToManyField('Tag', verbose_name=_('Tags'), blank=True, related_name='tagged_tracks')
    rubrics = models.ManyToManyField(
        'Rubric',
        verbose_name=_('Rubrics'),
        blank=True,
        related_name='rubricated_tracks',
    )

    uploadsFolder = getAudioTrackFolderName()

    # @see https://forum.djangoproject.com/t/how-to-pass-audio-file-from-model-to-template-in-django/11661
    audio_file = models.FileField(
        verbose_name=_('Audio file'),
        upload_to=uploadsFolder,
        blank=False,
        null=False,
    )
    preview_picture = models.ImageField(
        upload_to=uploadsFolder,
        blank=False,
        null=False,
        verbose_name=_('Preview picture'),
    )
    preview_picture_full = ImageSpecField(
        source='preview_picture',
        processors=[
            ResizeToFit(track_preview_picture_full_size, track_preview_picture_full_size),
        ],
        format='JPEG',
        options={'quality': track_preview_picture_jpeg_quality},
    )
    preview_picture_thumb = ImageSpecField(
        source='preview_picture',
        processors=[
            ResizeToFit(track_preview_picture_thumb_size, track_preview_picture_thumb_size),
        ],
        format='JPEG',
        options={'quality': track_preview_picture_jpeg_quality},
    )

    # Track status
    TRACK_STATUS = [
        ('PUBLISHED', _('Published')),
        ('HIDDEN', _('Hidden')),
        ('TEST', _('Test')),  # DEBUG!
    ]
    DEFAULT_TRACK_STATUS = TRACK_STATUS[0][0]
    track_status = models.TextField(
        _('Status'),
        choices=TRACK_STATUS,
        default=DEFAULT_TRACK_STATUS,
        help_text=_('Only published tracks will be shown'),
    )

    promote = models.BooleanField(_('Promote'), default=False, help_text=_('Promote on the main page'))

    for_members = models.BooleanField(
        _('For members only'),
        default=False,
        help_text=_('Show only for privileged members'),
    )

    played_count = models.BigIntegerField(
        blank=True,
        default=0,
        verbose_name=_('Played count'),
    )

    # Properties derived from the audio track file
    audio_duration = models.FloatField(null=True, verbose_name=_('Duration (seconds)'))
    audio_size = models.BigIntegerField(null=True, verbose_name=_('File size (bytes)'))

    # Timestamps
    # created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(verbose_name=_('Published at'), default=date.today)
    updated_at = models.DateField(verbose_name=_('Updated at'), auto_now=True)

    # Owner/creator
    published_by = models.ForeignKey(
        'User',
        verbose_name=_('Published by'),
        related_name='publisher',
        on_delete=models.DO_NOTHING,
    )
    updated_by = models.ForeignKey(
        'User',
        verbose_name=_('Updated by'),
        related_name='updater',
        on_delete=models.DO_NOTHING,
    )

    @property
    def lower_title(self) -> bool:
        # language = get_current_language()
        return self.title.lower()

    @property
    def active(self) -> bool:
        return self.status == 'PUBLISHED'

    @property
    def duration_formatted(track):
        return str(timedelta(seconds=round(track.audio_duration))) if track.audio_duration else '-'

    @property
    def size_formatted(track):
        return sizeofFmt(track.audio_size) if track.audio_size else '-'

    def save(self, *args, **kwargs):
        # Try to remove the old files...
        try:
            track = Track.objects.get(id=self.id)
            if (
                track.audio_file
                and self.audio_file
                and track.audio_file != self.audio_file
                and not str(track.audio_file).startswith('samples/')
            ):
                track.audio_file.delete(save=False)
            if (
                track.preview_picture
                and self.preview_picture
                and track.preview_picture != self.preview_picture
                and not str(track.preview_picture).startswith('samples/')
            ):
                track.preview_picture.delete(save=False)
        except Track.DoesNotExist:
            # Do nothing when a new object is creating
            pass
        # Call save first, to create a primary key
        super(Track, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'track_details',
            kwargs={
                'track_id': self.id,
            },
        )

    def __str__(self):
        items = [
            self.title,
            '[%d]' % self.id if LOCAL else None,
        ]
        info = ' '.join(map(str, filter(None, items)))
        return info  # f'Track(id={self.id}, title={self.title})'


@receiver(post_delete, sender=Track)
def on_track_delete(sender, instance: Track, using, **kwargs):
    _logger.info('[on_track_delete] On track delete' + repr(Track))
    try:
        # Try to remove uloaded files...
        if instance.audio_file:
            instance.audio_file.delete(save=False)
        if instance.preview_picture:
            instance.preview_picture.delete(save=False)
    except Exception as _:
        pass
