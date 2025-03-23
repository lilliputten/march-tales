from rest_framework import serializers

from core.logging import getDebugLogger

from ..models import Track

from .basic_plain_serializers import AuthorSerializer, RubricSerializer, TagSerializer

logger = getDebugLogger()


# Serializers define the API representation.
class TrackSerializer(serializers.HyperlinkedModelSerializer):

    # To use full data instead ids only
    # 0 - Only indices
    # 1 - Only full data
    # 2 - Both indices and data
    _full: int = 0

    # Fields...

    author = AuthorSerializer(read_only=True)
    rubrics = RubricSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    audio_file = serializers.SerializerMethodField('get_audio_file')

    def get_audio_file(self, obj):
        return obj.audio_file.url

    preview_picture = serializers.SerializerMethodField('get_preview_picture')

    def get_preview_picture(self, obj):
        # TODO: Use thumbnail/full images: preview_picture_thumb/preview_picture_full
        return obj.preview_picture.url

    rubric_ids = serializers.SerializerMethodField('get_rubric_ids')

    def get_rubric_ids(self, obj):
        return list(map(lambda it: it.id, obj.rubrics.all()))

    tag_ids = serializers.SerializerMethodField('get_tag_ids')

    def get_tag_ids(self, obj):
        return list(map(lambda it: it.id, obj.tags.all()))

    # Constructor
    def __init__(self, *args, full=False, **kwargs):
        self._full = full
        # logger.info(f'[track_serializers:TrackSerializer:__init__] full={full} args={args} kwargs={kwargs}')
        super().__init__(*args, **kwargs)

    # Fields list creator
    def get_default_field_names(self, declared_fields, model_info):
        send_data = self._full
        send_ids = not self._full or self._full == 2
        fields = (
            'id',
            # 'active',  # ???
            # 'duration_formatted',
            'title',
            'audio_duration',
            'audio_file',
            'audio_size',
            'description',
            'promote',
            'for_members',
            'played_count',
            'preview_picture',
            'published_at',
            'published_by_id',
            'track_status',
            'updated_at',
            'updated_by_id',
            'youtube_url',
            'author',
            # TODO: Use ids istead of fully serialized objects
            'rubric_ids' if send_ids else None,
            'rubrics' if send_data else None,
            'tag_ids' if send_ids else None,
            'tags' if send_data else None,
        )
        # logger.info(
        #     f'[track_serializers:TrackSerializer:get_default_field_names] send_data={send_data} send_ids={send_ids} fields={fields}'
        # )
        return list(filter(None, fields))

    class Meta:
        model = Track

        exclude = []

        # fields = (
        #     'id',
        #     # 'active',  # ???
        #     # 'duration_formatted',
        #     'title',
        #     'audio_duration',
        #     'audio_file',
        #     'audio_size',
        #     'description',
        #     'promote',
        #     'for_members',
        #     'played_count',
        #     'preview_picture',
        #     'published_at',
        #     'published_by_id',
        #     'track_status',
        #     'updated_at',
        #     'updated_by_id',
        #     'youtube_url',
        #     'author',
        #     # TODO: Use ids istead of fully serialized objects
        #     'rubric_ids',
        #     'rubrics',
        #     'tag_ids',
        #     'tags',
        # )
