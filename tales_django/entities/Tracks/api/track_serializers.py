from rest_framework import serializers

from ..models import Track, Tag, Rubric, Author

from .basic_plain_serializers import AuthorSerializer, RubricSerializer, TagSerializer


# Serializers define the API representation.
class TrackSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    rubrics = RubricSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    audio_file = serializers.SerializerMethodField('get_audio_file')

    def get_audio_file(self, obj):
        return obj.audio_file.url

    preview_picture = serializers.SerializerMethodField('get_preview_picture')

    def get_preview_picture(self, obj):
        return obj.preview_picture.url

    rubric_ids = serializers.SerializerMethodField('get_rubric_ids')

    def get_rubric_ids(self, obj):
        return list(map(lambda it: it.id, obj.rubrics.all()))

    tag_ids = serializers.SerializerMethodField('get_tag_ids')

    def get_tag_ids(self, obj):
        return list(map(lambda it: it.id, obj.tags.all()))

    class Meta:
        model = Track

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
            'rubric_ids',
            'rubrics',
            'tag_ids',
            'tags',
        )
