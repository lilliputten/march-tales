from translated_fields import TranslatedFieldAdmin, to_attribute

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib import admin
from django.db.models import Count, F
from django.db.models.functions import Lower

from ..models import Tag
from ..forms import TagAdminForm


@admin.register(Tag)
class TagAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    form = TagAdminForm
    list_display = [
        'text_translated',
        'promote',
        'tagged_tracks_count',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _tracks_count=Count('tracks', distinct=True),
            _text_translated=F('text_' + get_language()),
        )
        return queryset

    def text_translated(self, track):
        return track.text

    text_translated.admin_order_field = Lower('_text_translated')
    text_translated.short_description = _('text')

    def tagged_tracks_count(self, obj):
        return obj._tracks_count

    tagged_tracks_count.admin_order_field = '_tracks_count'
    tagged_tracks_count.short_description = _('tracks count')

    def get_ordering(self, request):
        return [Lower(to_attribute('text'))]
