from translated_fields import TranslatedFieldAdmin, to_attribute

from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Count, F
from django.db.models.functions import Lower

# from django.db.models.functions import Concat

from ..models import Author
from ..forms import AuthorAdminForm


@admin.register(Author)
class AuthorAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    form = AuthorAdminForm
    list_display = [
        'name_translated',
        # 'name',
        'promote',
        'tracks_count',
        'has_portrait',
    ]
    # fieldsets = [
    #     (_('Name'), {'fields': Author.name.fields}),
    #     (_('Description'), {'fields': Author.description.fields}),
    # ]

    def name_translated(self, track):
        return track.name

    name_translated.admin_order_field = Lower('_name_translated')
    name_translated.short_description = _('Name')

    def has_portrait(self, track):
        return True if track.portrait_picture else False

    has_portrait.admin_order_field = 'portrait_picture'

    has_portrait.short_description = _('Has portrait')
    has_portrait.boolean = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _tracks_count=Count('track', distinct=True),
            _name_translated=F('name_' + get_language()),
        )
        return queryset

    def tracks_count(self, obj):
        return obj._tracks_count

    tracks_count.admin_order_field = '_tracks_count'
    tracks_count.verbose_name = _('Tracks count')

    def get_ordering(self, request):
        return [Lower(to_attribute('name'))]
