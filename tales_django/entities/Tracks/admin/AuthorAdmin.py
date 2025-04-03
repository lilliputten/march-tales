from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from translated_fields import TranslatedFieldAdmin, to_attribute

from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Count, F
from django.db.models.functions import Lower

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.sites import unfold_admin_site

from ..models import Author

# from ..forms import AuthorAdminForm


@admin.action(description=_('Promote'))
def promote_action(modeladmin, request, queryset):
    queryset.update(promote=True)


@admin.action(description=_('No promote'))
def no_promote_action(modeladmin, request, queryset):
    queryset.update(promote=False)


@admin.register(Author, site=unfold_admin_site)
class AuthorAdmin(TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    actions = [
        promote_action,
        no_promote_action,
    ]
    list_display = [
        'name_translated',
        # 'name',
        'tracks_count',
        'promote',
        'has_portrait',
        # 'published_at',
        'updated_at',
    ]
    readonly_fields = (
        'published_at',
        'updated_at',
    )
    search_fields = [
        'name_en',
        'name_ru',
        # 'short_description_en',
        # 'short_description_ru',
        # 'description_en',
        # 'description_ru',
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
