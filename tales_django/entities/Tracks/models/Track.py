# from django.utils.translation import ugettext_lazy as _

from datetime import date
from django.db import models
from django.db.models import Model

# from core.appEnv import LOCAL

from core.appEnv import LOCAL
from tales_django.core.helpers.audio import getAudioTrackFolderName


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

    def __str__(self):
        items = [
            'Track',
            self.title,
            '[%d]' % self.id if LOCAL else None,
        ]
        info = ' '.join(filter(None, map(str, items)))
        return info
