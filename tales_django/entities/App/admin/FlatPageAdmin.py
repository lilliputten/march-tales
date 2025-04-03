from django.contrib.flatpages.admin import FlatPageAdmin as BaseFlatPageAdmin

from django.contrib import admin
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from translated_fields import TranslatedFieldAdmin

from unfold.admin import ModelAdmin as UnfoldModelAdmin


from tales_django.sites import unfold_admin_site

from ..forms import FlatPageForm
from ..models import FlatPage, BaseFlatPage


# @see .venv/Lib/site-packages/django/contrib/flatpages/models.py


admin.site.unregister(BaseFlatPage)


# @admin.register(FlatPage, site=unfold_admin_site)
@admin.register(FlatPage, site=unfold_admin_site)
class FlatPageAdmin(
    BaseFlatPageAdmin,
    TranslatedFieldAdmin,
    ImportExportModelAdmin,
    ExportActionModelAdmin,
    UnfoldModelAdmin,
):
    form = FlatPageForm
    import_form_class = ImportForm
    export_form_class = ExportForm
    fieldsets = [
        (
            _('Basic Settings'),
            {
                # 'classes': ['collapse', '--opened-by-default'],
                'fields': [
                    'url',
                    'sites',
                ],
            },
        ),
        (
            _('Title'),
            {
                'classes': ['collapse'],
                'fields': (
                    'page_title_ru',
                    'page_title_en',
                )
            },
        ),
        (
            _('Content'),
            {
                'classes': ['collapse'],
                'fields': (
                    'page_content_ru',
                    'page_content_en',
                )
            },
        ),
        (
            _('Advanced options'),
            {
                'classes': ['collapse'],
                'fields': [
                    # 'enable_comments',
                    'registration_required',
                    'template_name',
                ],
            },
        ),
        (
            _('Information'),
            {
                'classes': ['collapse'],
                'fields': (
                    'published_at',
                    'updated_at',
                ),
            },
        ),
    ]
    list_display = [
        'url',
        # 'page_title',
        'title_translated',
        'registration_required',
        # 'published_at',
        'updated_at',
    ]
    readonly_fields = (
        'published_at',
        'updated_at',
    )

    ordering = [
        'url',
        'page_title_ru',
        'registration_required',
    ]
    search_fields = [
        'url',
        'page_title_en',
        'page_title_ru',
    ]

    def title_translated(self, track):
        return track.page_title

    title_translated.admin_order_field = Lower('_title_translated')
    title_translated.short_description = _('Title')
