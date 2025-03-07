from rest_framework import serializers

from ..models import Track, Tag, Rubric, Author

from .basic_plain_serializers import AuthorSerializer, RubricSerializer, TagSerializer


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    portrait_picture = serializers.SerializerMethodField()

    def get_portrait_picture(self, obj):
        return obj.portrait_picture.url

    track_ids = serializers.SerializerMethodField('get_track_ids')

    def get_track_ids(self, obj):
        tracks = Track.objects.filter(track_status='PUBLISHED', author__id=obj.id)
        return list(map(lambda t: t.id, tracks))

    rubrics = serializers.SerializerMethodField('get_rubrics')

    def get_rubrics(self, obj):
        track_ids = self.get_track_ids(obj)
        rubrics = Rubric.objects.filter(tracks__id__in=track_ids)
        serializer = RubricSerializer(rubrics, read_only=True, many=True)
        return serializer.data

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        track_ids = self.get_track_ids(obj)
        tags = Tag.objects.filter(tracks__id__in=track_ids)
        serializer = TagSerializer(tags, read_only=True, many=True)
        return serializer.data

    # DEMO: Full serialized tracks example
    # tracks = serializers.SerializerMethodField('get_tracks')
    # def get_tracks(self, obj):
    #     language = translation.get_language()
    #     tracks = (
    #         Track.objects.filter(track_status='PUBLISHED', author__id=obj.id)
    #         .order_by('-published_at', f'title_{language}')
    #     )
    #     serializer = TrackSerializer(tracks, read_only=True, many=True)
    #     return serializer.data

    class Meta:
        model = Author

        fields = (
            'id',
            'name',
            'short_description',
            'description',
            'portrait_picture',
            'promote',
            # Related data...
            'track_ids',
            'rubrics',
            'tags',
        )
