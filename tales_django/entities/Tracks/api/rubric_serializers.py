from rest_framework import serializers

from tales_django.core.model_helpers import get_currrent_django_language

from ..models import Track, Tag, Rubric, Author

from .basic_plain_serializers import AuthorSerializer, RubricSerializer, TagSerializer


class RubricSerializer(serializers.HyperlinkedModelSerializer):
    track_ids = serializers.SerializerMethodField('get_track_ids')

    def get_track_ids(self, obj):
        language = get_currrent_django_language()
        tracks = (
            Track.objects.filter(track_status='PUBLISHED', rubric__id=obj.id)
            .distinct()
            .order_by('-published_at', f'title_{language}')
        )
        # tracks = Track.objects.filter(track_status='PUBLISHED', rubric__id=obj.id)
        return list(map(lambda t: t.id, tracks))

    authors = serializers.SerializerMethodField('get_authors')

    def get_authors(self, obj):
        language = get_currrent_django_language()
        track_ids = self.get_track_ids(obj)
        authors = Author.objects.filter(track__id__in=track_ids).distinct().order_by(f'name_{language}')
        # authors = Author.objects.filter(track__id__in=track_ids)
        serializer = AuthorSerializer(authors, read_only=True, many=True)
        return serializer.data

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        language = get_currrent_django_language()
        track_ids = self.get_track_ids(obj)
        tags = Tag.objects.filter(tracks__id__in=track_ids).distinct().order_by(f'text_{language}')
        # tags = Tag.objects.filter(tracks__id__in=track_ids)
        serializer = TagSerializer(tags, read_only=True, many=True)
        return serializer.data

    class Meta:
        model = Rubric

        fields = (
            'id',
            'text',
            'promote',
            # Related data...
            'track_ids',
            'authors',
            'tags',
        )
