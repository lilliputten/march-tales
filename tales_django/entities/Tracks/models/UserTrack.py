from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.logging import getDebugLogger

logger = getDebugLogger()


class UserTrack(models.Model):
    class Meta:
        verbose_name = _('user track')
        verbose_name_plural = _('user tracks')

    # Relations
    user = models.ForeignKey(
        'User', verbose_name=_('User'), related_name='user_track_relation', on_delete=models.CASCADE
    )
    track = models.ForeignKey(
        'Track', verbose_name=_('Track'), related_name='track_user_relation', on_delete=models.CASCADE
    )

    # Favorite
    is_favorite = models.BooleanField(
        _('Is favorite'),
        default=False,
        help_text=_('Is track in favorites for the current user?'),
    )
    favorited_at = models.DateTimeField(
        _('Added to favorites'),
        null=True,
        help_text=_('When track was added/removed to/from favorites'),
    )

    # Playback
    played_count = models.BigIntegerField(
        _('Played count'),
        default=0,
        help_text=_('Played count by this user'),
    )
    position = models.FloatField(
        _('Playback position'),
        default=0,
        help_text=_('Last playback position (seconds)'),
    )
    played_at = models.DateTimeField(
        _('Last played'),
        null=True,
        help_text=_('Last played time'),
    )

    @property
    def position_formatted(track):
        return str(timedelta(seconds=round(track.position))) if track.position else '-'

    # Info
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
