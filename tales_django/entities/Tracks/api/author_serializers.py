from rest_framework import serializers

from .track_serializers import TrackSerializer

from ..models import Tag, Rubric, Author


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
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(read_only=True, many=True)
    # rubrics = RubricSerializer(read_only=True, many=True)
    # tags = TagSerializer(read_only=True, many=True)

    audio_file = serializers.SerializerMethodField()

    def get_audio_file(self, obj):
        return obj.audio_file.url

    portrait_picture = serializers.SerializerMethodField()

    def get_portrait_picture(self, obj):
        return obj.portrait_picture.url

    class Meta:
        model = Author

        fields = (
            'id',
            'name',
            'portrait_picture',
            'tracks',
            # 'rubrics',
            # 'tags',
        )
