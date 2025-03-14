from translated_fields import TranslatedFieldAdmin, to_attribute

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from django.contrib import admin
from django.db.models import Count, F
from django.db.models.functions import Lower

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.sites import unfold_admin_site

from ..models import Rubric

# from ..forms import RubricAdminForm


@admin.action(description=_('Promote'))
def promote_action(modeladmin, request, queryset):
    queryset.update(promote=True)


@admin.action(description=_('No promote'))
def no_promote_action(modeladmin, request, queryset):
    queryset.update(promote=False)


@admin.register(Rubric, site=unfold_admin_site)
class RubricAdmin(TranslatedFieldAdmin, UnfoldModelAdmin):
    # form = RubricAdminForm
    actions = [
        promote_action,
        no_promote_action,
    ]
    list_display = [
        'text_translated',
        'promote',
        'rubricated_tracks_count',
    ]
    search_fields = [
        'text_en',
        'text_ru',
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

    def rubricated_tracks_count(self, obj):
        return obj._tracks_count

    rubricated_tracks_count.admin_order_field = '_tracks_count'
    rubricated_tracks_count.short_description = _('tracks count')

    def get_ordering(self, request):
        return [Lower(to_attribute('text'))]
