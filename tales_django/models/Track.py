# from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models import Model


uploadsFolder = 'tracks'


class Track(Model):
    title = models.TextField(unique=True, blank=False, null=False, max_length=150, verbose_name='track title', help_text='Required. 150 characters or fewer. Track title')
    description = models.TextField(blank=True, null=False, max_length=512, verbose_name='description')
    youtube_url = models.URLField(blank=True, null=False, max_length=150)
    tags_list = models.TextField(blank=True, null=False, max_length=150)

    # @see https://forum.djangoproject.com/t/how-to-pass-audio-file-from-model-to-template-in-django/11661
    preview_picture = models.ImageField(upload_to=uploadsFolder)
    audio_file = models.FileField(upload_to=uploadsFolder, blank=False, null=False)

    TRACK_STATUS = [
        ('HIDDEN', 'Hidden'),
        ('PUBLISHED', 'Published'),
    ]
    DEFAULT_TRACK_STATUS = TRACK_STATUS[0][0]
    track_status = models.TextField(choices=TRACK_STATUS, default=DEFAULT_TRACK_STATUS)

    # Owner/creator
    created_by = models.ForeignKey('User', related_name='creator', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey('User', related_name='updater', on_delete=models.DO_NOTHING)

    # Timestamps
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def active(self) -> bool:
        return self.status == 'PUBLISHED'

    def __str__(self):
        items = [
            '[%d]' % self.id,
            self.title,
        ]
        info = ', '.join(filter(None, map(str, items)))
        return info
