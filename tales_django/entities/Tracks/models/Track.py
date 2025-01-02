# from django.utils.translation import ugettext_lazy as _

from datetime import date
from django.db import models
from django.db.models import Model
from django.db.models.signals import post_delete
from django.dispatch import receiver

from core.appEnv import LOCAL
from core.logging import getDebugLogger
from tales_django.core.helpers.audio import getAudioTrackFolderName


_logger = getDebugLogger()


class Track(Model):
    title = models.TextField(
        unique=False,
        blank=False,
        null=False,
        max_length=150,
        verbose_name='track title',
        help_text='Required. 150 characters or fewer. Track title',
    )
    description = models.TextField(blank=True, null=False, max_length=512, verbose_name='Description')
    youtube_url = models.URLField(blank=True, null=False, max_length=150, verbose_name='YouTube video link url')
    tags_list = models.TextField(blank=True, null=False, max_length=150)

    uploadsFolder = getAudioTrackFolderName()

    # @see https://forum.djangoproject.com/t/how-to-pass-audio-file-from-model-to-template-in-django/11661
    audio_file = models.FileField(
        upload_to=uploadsFolder,
        blank=False,
        null=False,
    )
    preview_picture = models.ImageField(upload_to=uploadsFolder, blank=True, null=True)

    # Track status
    TRACK_STATUS = [
        ('PUBLISHED', 'Published'),
        ('HIDDEN', 'Hidden'),
    ]
    DEFAULT_TRACK_STATUS = TRACK_STATUS[0][0]
    track_status = models.TextField(choices=TRACK_STATUS, default=DEFAULT_TRACK_STATUS)

    for_members = models.BooleanField(default=False, verbose_name='For members only')

    # Properties derived from the audio track file
    audio_duration = models.BigIntegerField(null=True, help_text='Duration (seconds)')
    audio_size = models.BigIntegerField(null=True, help_text='File size (bytes)')

    # Timestamps
    # created_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(default=date.today)
    updated_at = models.DateField(auto_now=True)

    # Owner/creator
    created_by = models.ForeignKey('User', related_name='creator', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey('User', related_name='updater', on_delete=models.DO_NOTHING)

    @property
    def active(self) -> bool:
        return self.status == 'PUBLISHED'

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
