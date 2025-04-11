from rest_framework import serializers

from core.logging import getDebugLogger

from ..models import UserTrack

logger = getDebugLogger()


# Serializers define the API representation.
class UserTrackSerializer(serializers.HyperlinkedModelSerializer):
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

    # Fields list creator
    def get_default_field_names(self, declared_fields, model_info):
        # send_data = self._full
        # send_ids = not self._full or self._full == 2
        fields = (
            'id',
            'user_id',
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
