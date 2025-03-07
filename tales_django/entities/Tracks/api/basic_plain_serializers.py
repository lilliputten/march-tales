from rest_framework import serializers

from ..models import Track, Tag, Rubric, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    portrait_picture = serializers.SerializerMethodField('get_portrait_picture')

    def get_portrait_picture(self, obj):
        return obj.portrait_picture.url

    class Meta:
        model = Author
        fields = (
            'id',
            'name',
            'portrait_picture',
            'promote',
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
