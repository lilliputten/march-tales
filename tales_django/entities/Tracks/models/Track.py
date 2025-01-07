# from django.utils.translation import ugettext_lazy as _

from datetime import date
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model
from django.db.models.signals import post_delete
from django.dispatch import receiver

from core.helpers.files import sizeofFmt
from core.appEnv import LOCAL
from core.logging import getDebugLogger
from tales_django.core.helpers.audio import getAudioTrackFolderName


_logger = getDebugLogger()


class Track(Model):
    class Meta:
        verbose_name = _('track')
        verbose_name_plural = _('tracks')

    title = models.TextField(
        unique=False,
        blank=False,
        null=False,
        max_length=150,
        verbose_name='track title',
        help_text='Required. 150 characters or fewer. The track title text.',
    )
    description = models.TextField(
        blank=True,
        null=False,
        max_length=512,
        help_text='Optional description, up to 512 characters.',
    )
    youtube_url = models.URLField(blank=True, null=False, max_length=150, help_text='YouTube video link url')

    author = models.ForeignKey('Author', blank=True, null=True, on_delete=models.DO_NOTHING)

    tags = models.ManyToManyField('Tag', blank=True, related_name='tagged_tracks')
    rubrics = models.ManyToManyField('Rubric', blank=True, related_name='rubricated_tracks')

    uploadsFolder = getAudioTrackFolderName()

    # @see https://forum.djangoproject.com/t/how-to-pass-audio-file-from-model-to-template-in-django/11661
    audio_file = models.FileField(
        upload_to=uploadsFolder,
        blank=False,
        null=False,
    )
    preview_picture = models.ImageField(upload_to=uploadsFolder, blank=True)

    # Track status
    TRACK_STATUS = [
        ('PUBLISHED', 'Published'),
        ('HIDDEN', 'Hidden'),
        ('TEST', 'Test'),  # DEBUG!
    ]
    DEFAULT_TRACK_STATUS = TRACK_STATUS[0][0]
    track_status = models.TextField(choices=TRACK_STATUS, default=DEFAULT_TRACK_STATUS)

    for_members = models.BooleanField(default=False, verbose_name='For members only')

    # Properties derived from the audio track file
    audio_duration = models.BigIntegerField(null=True, help_text='Duration (seconds)')
    audio_size = models.BigIntegerField(null=True, help_text='File size (bytes)')

    # Timestamps
    # created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(default=date.today)
    updated_at = models.DateField(auto_now=True)

    # Owner/creator
    published_by = models.ForeignKey('User', related_name='publisher', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey('User', related_name='updater', on_delete=models.DO_NOTHING)

    @property
    def active(self) -> bool:
        return self.status == 'PUBLISHED'

    @property
    def duration_formatted(track):
        return str(timedelta(seconds=track.audio_duration)) if track.audio_duration else '-'

    @property
    def size_formatted(track):
        return sizeofFmt(track.audio_size) if track.audio_size else '-'

    def save(self, *args, **kwargs):
        # Try to remove the old files...
        try:
            track = Track.objects.get(id=self.id)
            if track.audio_file and self.audio_file and track.audio_file != self.audio_file:
                track.audio_file.delete(save=False)
            if track.preview_picture and self.preview_picture and track.preview_picture != self.preview_picture:
                track.preview_picture.delete(save=False)
        except Track.DoesNotExist:
            # Do nothing when a new object is creating
            pass
        # Call save first, to create a primary key
        super(Track, self).save(*args, **kwargs)

    def __str__(self):
        items = [
            'Track',
            self.title,
            '[%d]' % self.id if LOCAL else None,
        ]
        info = ' '.join(filter(None, map(str, items)))
        return info


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
