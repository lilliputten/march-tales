from rest_framework import serializers

from tales_django.core.model_helpers import get_current_language

from ..models import Track, Tag, Rubric, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    portrait_picture = serializers.SerializerMethodField('get_portrait_picture')

    def get_portrait_picture(self, obj):
        return obj.portrait_picture.url

    track_ids = serializers.SerializerMethodField('get_track_ids')

    def get_track_ids(self, obj):
        language = get_current_language()
        tracks = (
            Track.objects.filter(track_status='PUBLISHED', author__id=obj.id)
            .distinct()
            .order_by('-published_at', f'title_{language}')
        )
        # tracks = Track.objects.filter(track_status='PUBLISHED', author__id=obj.id)
        return list(map(lambda t: t.id, tracks))

    class Meta:
        model = Author
        fields = (
            'id',
            'name',
            'portrait_picture',
            'promote',
            'track_ids',
        )


class RubricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rubric
        fields = (
            'id',
            'promote',
            'text',
        )


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'promote',
            'promote',
            'text',
        )
