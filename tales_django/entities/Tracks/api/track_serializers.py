from rest_framework import serializers

from ..models import Track, Tag, Rubric, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    portrait_picture = serializers.SerializerMethodField()

    def get_portrait_picture(self, obj):
        return obj.portrait_picture.url

    class Meta:
        model = Author
        fields = (
            'id',
            'name',
            'portrait_picture',
        )


class RubricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rubric
        fields = (
            'id',
            'text',
        )


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'text',
        )


# Serializers define the API representation.
class TrackSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    rubrics = RubricSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    audio_file = serializers.SerializerMethodField()

    def get_audio_file(self, obj):
        return obj.audio_file.url

    preview_picture = serializers.SerializerMethodField()

    def get_preview_picture(self, obj):
        return obj.preview_picture.url

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
            'rubrics',
            'tags',
        )
