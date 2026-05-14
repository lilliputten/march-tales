from rest_framework import serializers

from tales_django.core.model_helpers import get_current_language

from ..models import Series, Track
from .basic_plain_serializers import AuthorSerializer, RubricSerializer, TagSerializer


class SeriesSerializer(serializers.HyperlinkedModelSerializer):

    # To use full data instead ids only
    # 0 - Only indices
    # 1 - Only full data
    # 2 - Both indices and data
    _full: int = 0

    tracks_count = serializers.IntegerField(read_only=True)
    published_tracks_count = serializers.IntegerField(read_only=True)

    track_ids = serializers.SerializerMethodField('get_track_ids')

    def get_track_ids(self, obj):
        language = get_current_language()
        tracks = (
            obj.tracks.filter(track_status='PUBLISHED')
            .distinct()
            .order_by('series_order', '-published_at', f'title_{language}')
        )
        return list(map(lambda t: t.id, tracks))

    tracks = serializers.SerializerMethodField('get_tracks')

    def get_tracks(self, obj):
        language = get_current_language()
        tracks = (
            obj.tracks.filter(track_status='PUBLISHED')
            .distinct()
            .order_by('series_order', '-published_at', f'title_{language}')
        )

        # Only serialize tracks if full data is requested
        if self._full >= 1:
            from .track_serializers import TrackSerializer

            full = self._full if self._full <= 1 else 0  # Convert 2 to 0 for compact tracks
            return TrackSerializer(tracks, full=full, read_only=True, many=True, context=self.context).data
        return []

    author_ids = serializers.SerializerMethodField('get_author_ids')

    def get_author_ids(self, obj):
        tracks = obj.tracks.filter(track_status='PUBLISHED').distinct()
        authors = tracks.values_list('author', flat=True).distinct()
        return list(filter(None, authors))

    authors = serializers.SerializerMethodField('get_authors')

    def get_authors(self, obj):
        if self._full >= 1:
            tracks = obj.tracks.filter(track_status='PUBLISHED').distinct()
            authors = tracks.select_related('author').values_list('author', flat=True).distinct()
            authors = list(filter(None, authors))
            from ..models import Author

            unique_authors = Author.objects.filter(id__in=authors)
            return AuthorSerializer(unique_authors, read_only=True, many=True).data
        return []

    rubric_ids = serializers.SerializerMethodField('get_rubric_ids')

    def get_rubric_ids(self, obj):
        tracks = obj.tracks.filter(track_status='PUBLISHED').distinct()
        rubrics = tracks.prefetch_related('rubrics').values_list('rubrics', flat=True).distinct()
        return list(filter(None, rubrics))

    rubrics = serializers.SerializerMethodField('get_rubrics')

    def get_rubrics(self, obj):
        if self._full >= 1:
            tracks = obj.tracks.filter(track_status='PUBLISHED').distinct()
            rubrics = tracks.prefetch_related('rubrics').values_list('rubrics', flat=True).distinct()
            rubrics = list(filter(None, rubrics))
            from ..models import Rubric

            unique_rubrics = Rubric.objects.filter(id__in=rubrics)
            return RubricSerializer(unique_rubrics, read_only=True, many=True).data
        return []

    tag_ids = serializers.SerializerMethodField('get_tag_ids')

    def get_tag_ids(self, obj):
        tracks = obj.tracks.filter(track_status='PUBLISHED').distinct()
        tags = tracks.prefetch_related('tags').values_list('tags', flat=True).distinct()
        # Filter out None values that can occur when tracks don't have tags
        return list(filter(None, tags))

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        if self._full >= 1:
            tracks = obj.tracks.filter(track_status='PUBLISHED').distinct()
            tags = tracks.prefetch_related('tags').values_list('tags', flat=True).distinct()
            # Filter out None values that can occur when tracks don't have tags
            tags = list(filter(None, tags))
            from ..models import Tag

            unique_tags = Tag.objects.filter(id__in=tags)
            return TagSerializer(unique_tags, read_only=True, many=True).data
        return []

    def __init__(self, *args, **kwargs):
        self._full = kwargs.pop('full', 0)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Series
        fields = (
            'id',
            'title',
            'description',
            'promote',
            'is_visible',
            'created_at',
            'updated_at',
            # Count fields
            'tracks_count',
            'published_tracks_count',
            # Related data - always include IDs
            'track_ids',
            'author_ids',
            'rubric_ids',
            'tag_ids',
            # Full data - only included when full=1
            'tracks',
            'authors',
            'rubrics',
            'tags',
        )
