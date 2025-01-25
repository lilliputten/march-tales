from rest_framework import serializers

from ..models import Track, Tag, Rubric, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'name',
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

    class Meta:
        model = Track
        fields = (
            'id',
            'title',
            # 'description',
            'youtube_url',
            'track_status',
            # 'author_id',
            'author',
            'tags',
            'rubrics',
            'audio_file',
            'audio_duration',
            'audio_size',
            'preview_picture',
            'for_members',
            'played_count',
            'published_at',
            # 'favorited_users',
        )
