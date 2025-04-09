from rest_framework import serializers

from core.logging import getDebugLogger

from ..models import UserTrack

# from .basic_plain_serializers import UserSerializer
from .track_serializers import TrackSerializer

logger = getDebugLogger()


# Serializers define the API representation.
class UserTrackSerializer(serializers.HyperlinkedModelSerializer):

    # To use full data instead ids only (UNUSED)
    # 0 - Only indices
    # 1 - Only full data
    # 2 - Both indices and data
    _full: int = 0

    # Fields...

    favorited_at_sec = serializers.SerializerMethodField('get_favorited_at_sec')
    played_at_sec = serializers.SerializerMethodField('get_played_at_sec')
    updated_at_sec = serializers.SerializerMethodField('get_updated_at_sec')

    def get_favorited_at_sec(self, obj):
        return round(obj.favorited_at.timestamp()) if obj.favorited_at is not None else None

    def get_played_at_sec(self, obj):
        return round(obj.played_at.timestamp()) if obj.played_at is not None else None

    def get_updated_at_sec(self, obj):
        return round(obj.updated_at.timestamp()) if obj.updated_at is not None else None

    # Objects (will be required for `full` data, not used at the moment)
    # user = UserSerializer(read_only=False, many=False)
    # track = TrackSerializer(read_only=False, many=False)

    # Constructor
    def __init__(self, *args, full=False, **kwargs):
        self._full = full
        super().__init__(*args, **kwargs)

    # Fields list creator
    def get_default_field_names(self, declared_fields, model_info):
        # send_data = self._full
        # send_ids = not self._full or self._full == 2
        fields = (
            'id',
            # Use ids istead of fully serialized objects if no `full` parameter provided
            'user_id',  #  if send_ids else None,
            # 'user' if send_data else None,
            'track_id',
            'is_favorite',
            'played_count',
            'position',
            'favorited_at_sec',
            'played_at_sec',
            'updated_at_sec',
        )
        return list(filter(None, fields))

    class Meta:
        model = UserTrack

        exclude = []
