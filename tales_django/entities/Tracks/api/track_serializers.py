from rest_framework import serializers

from ..models import Track, Tag, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'name',
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
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = (
            'title',
            # 'author_id',
            'author',
            'tags',
            'audio_file',
            'for_members',
            'played_count',
            # 'favorited_users',
        )
