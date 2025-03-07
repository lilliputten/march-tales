from rest_framework import serializers

from ..models import Track, Tag, Rubric, Author

from .basic_plain_serializers import AuthorSerializer, RubricSerializer


class TagSerializer(serializers.HyperlinkedModelSerializer):
    track_ids = serializers.SerializerMethodField('get_track_ids')

    def get_track_ids(self, obj):
        tracks = Track.objects.filter(track_status='PUBLISHED', tag__id=obj.id)
        return list(map(lambda t: t.id, tracks))

    authors = serializers.SerializerMethodField('get_authors')

    def get_authors(self, obj):
        track_ids = self.get_track_ids(obj)
        authors = Author.objects.filter(track__id__in=track_ids)
        serializer = AuthorSerializer(authors, read_only=True, many=True)
        return serializer.data

    rubrics = serializers.SerializerMethodField('get_rubrics')

    def get_rubrics(self, obj):
        track_ids = self.get_track_ids(obj)
        rubrics = Rubric.objects.filter(tracks__id__in=track_ids)
        serializer = RubricSerializer(rubrics, read_only=True, many=True)
        return serializer.data

    class Meta:
        model = Tag

        fields = (
            'id',
            'text',
            'promote',
            # Related data...
            'track_ids',
            'authors',
            'rubrics',
        )
