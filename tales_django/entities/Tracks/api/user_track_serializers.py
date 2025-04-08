from rest_framework import serializers

from core.logging import getDebugLogger

from ..models import UserTrack

# from .basic_plain_serializers import UserSerializer
from .track_serializers import TrackSerializer

logger = getDebugLogger()


# Serializers define the API representation.
class UserTrackSerializer(serializers.HyperlinkedModelSerializer):

    # To use full data instead ids only
    # 0 - Only indices
    # 1 - Only full data
    # 2 - Both indices and data
    _full: int = 0

    # Fields...

    # user = UserSerializer(read_only=False, many=False)
    track = TrackSerializer(read_only=False, many=False)

    # Constructor
    def __init__(self, *args, full=False, **kwargs):
        self._full = full
        # logger.info(f'[user_track_serializers:UserTrackSerializer:__init__] full={full} args={args} kwargs={kwargs}')
        super().__init__(*args, **kwargs)

    # Fields list creator
    def get_default_field_names(self, declared_fields, model_info):
        send_data = self._full
        send_ids = not self._full or self._full == 2
        fields = (
            'id',
            # Use ids istead of fully serialized objects if no `full` parameter provided
            'user_id' if send_ids else None,
            'user' if send_data else None,
            'track_id' if send_ids else None,
            # 'track' if send_data else None,
            'is_favorite',
            'favorited_at',
            'played_count',
            'position',
            'played_at',
        )
        # logger.info(
        #     f'[user_track_serializers:UserTrackSerializer:get_default_field_names] send_data={send_data} send_ids={send_ids} fields={fields}'
        # )
        return list(filter(None, fields))

    class Meta:
        model = UserTrack

        exclude = []
