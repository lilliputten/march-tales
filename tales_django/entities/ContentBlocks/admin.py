import textwrap

from django.contrib import admin
from django.db.models import F, Q
from django.db.models.functions import Lower
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from translated_fields import TranslatedFieldAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.core.helpers import remove_html_tags
from tales_django.core.model_helpers import localized_field_names
from tales_django.sites import unfold_admin_site

from .forms import ContentBlocksForm
from .models import ContentBlocks


@admin.action(description=_('Make string'))
def make_string(modeladmin, request, queryset):
    queryset.update(type=ContentBlocks.STRING)


@admin.action(description=_('Make block'))
def make_block(modeladmin, request, queryset):
    queryset.update(type=ContentBlocks.BLOCK)


@admin.action(description=_('Make rich block'))
def make_rich_block(modeladmin, request, queryset):
    queryset.update(type=ContentBlocks.RICH_BLOCK)


@admin.register(ContentBlocks, site=unfold_admin_site)
class ContentBlocksAdmin(
    TranslatedFieldAdmin,
    ImportExportModelAdmin,
    ExportActionModelAdmin,
    UnfoldModelAdmin,
):
    actions = [
        make_string,
        make_block,
        make_rich_block,
    ]

    form = ContentBlocksForm
    content_fields = localized_field_names('content')
    fieldsets = (
        (
            _('Basic Settings'),
            {
                'classes': ['columns'],
                'fields': [
                    'name',
                    'type',
                ],
            },
        ),
        (
            _('Content'),
            {
                'classes': ['columns'],
                'fields': content_fields,
            },
        ),
        (
            _('Information'),
            {
                'classes': ['collapse', 'columns'],
                'fields': (
                    'created_at',
                    'updated_at',
                ),
            },
        ),
    )

    list_display = [
        'name',
        'content_short',
        'type',
        'updated_at',
    ]
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    search_fields = [
        'url',
        'name',
        *content_fields,
    ]

    list_filter = [
        'type',
        'created_at',
        'updated_at',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _content_short=F('content_' + get_language()),
        )
        return queryset

    def content_short(self, obj):
        str = remove_html_tags(obj.content)
        return textwrap.shorten(str, width=40, placeholder='...')

    content_short.admin_order_field = Lower('_content_short')
    content_short.short_description = _('content')
