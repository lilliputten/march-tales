from translated_fields import TranslatedField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage as BaseFlatPage
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model

from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from translated_fields import TranslatedFieldAdmin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from tales_django.core.model_helpers import get_non_empty_localized_model_field_attrgetter

from tales_django.sites import unfold_admin_site


class FlatPage(BaseFlatPage):
    class Meta:
        verbose_name = _('Flat page')
        verbose_name_plural = _('Flat pages')

    title = TranslatedField(
        models.CharField(
            _('title'),
            max_length=200,
            default='',
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )
    content = TranslatedField(
        models.TextField(
            _('content'),
            blank=True,
            default='',
        ),
        attrgetter=get_non_empty_localized_model_field_attrgetter,
    )

    # text = TranslatedField(
    #     models.TextField(
    #         _('Text'),
    #         unique=False,
    #         blank=False,
    #         null=False,
    #         max_length=256,
    #     ),
    #     attrgetter=get_non_empty_localized_model_field_attrgetter,
    # )
    #
    # pass


# Define a new FlatPageAdmin
# @admin.register(FlatPage, site=unfold_admin_site)
@admin.register(FlatPage, site=unfold_admin_site)
class CustomFlatPageAdmin(
    FlatPageAdmin, TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin
):
    import_form_class = ImportForm
    export_form_class = ExportForm
    fieldsets = [
        (
            _('Basic Settings'),
            {
                'fields': [
                    'url',
                    # 'title',
                    # 'content',
                    # 'sites',
                ],
            },
        ),
        (
            _('Title'),
            {
                'fields': (
                    'title_ru',
                    'title_en',
                )
            },
        ),
        (
            _('Content'),
            {
                'fields': (
                    'content_ru',
                    'content_en',
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
                    'sites',
                ],
            },
        ),
    ]
    # pass


# Re-register FlatPageAdmin
admin.site.unregister(BaseFlatPage)
# admin.site.register(FlatPage, CustomFlatPageAdmin)
