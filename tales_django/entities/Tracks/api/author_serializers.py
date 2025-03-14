from rest_framework import serializers

from tales_django.core.model_helpers import get_currrent_django_language

from ..models import Track, Tag, Rubric, Author

from .basic_plain_serializers import AuthorSerializer, RubricSerializer, TagSerializer


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    portrait_picture = serializers.SerializerMethodField()

    def get_portrait_picture(self, obj):
        return obj.portrait_picture.url

    track_ids = serializers.SerializerMethodField('get_track_ids')

    def get_track_ids(self, obj):
        language = get_currrent_django_language()
        tracks = (
            Track.objects.filter(track_status='PUBLISHED', author__id=obj.id)
            .distinct()
            .order_by('-published_at', f'title_{language}')
        )
        # tracks = Track.objects.filter(track_status='PUBLISHED', author__id=obj.id)
        return list(map(lambda it: it.id, tracks))

    rubrics = serializers.SerializerMethodField('get_rubrics')

    def get_rubrics(self, obj):
        language = get_currrent_django_language()
        track_ids = self.get_track_ids(obj)
        rubrics = Rubric.objects.filter(tracks__id__in=track_ids).distinct().order_by(f'text_{language}')
        serializer = RubricSerializer(rubrics, read_only=True, many=True)
        return serializer.data

    rubric_ids = serializers.SerializerMethodField('get_rubric_ids')

    def get_rubric_ids(self, obj):
        rubrics_data = self.get_rubrics(obj)
        return list(map(lambda it: it['id'], rubrics_data))

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        language = get_currrent_django_language()
        track_ids = self.get_track_ids(obj)
        tags = Tag.objects.filter(tracks__id__in=track_ids).distinct().order_by(f'text_{language}')
        # tags = Tag.objects.filter(tracks__id__in=track_ids)
        serializer = TagSerializer(tags, read_only=True, many=True)
        return serializer.data

    tag_ids = serializers.SerializerMethodField('get_tag_ids')

    def get_tag_ids(self, obj):
        tags_data = self.get_tags(obj)
        return list(map(lambda it: it['id'], tags_data))

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
            # TODO: Use ids istead of fully serialized objects
            'rubric_ids',
            'rubrics',
            'tag_ids',
            'tags',
        )
