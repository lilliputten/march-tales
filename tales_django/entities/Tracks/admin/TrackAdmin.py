import traceback

from translated_fields import TranslatedFieldAdmin, to_attribute

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm   # , SelectableFieldsExportForm

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from django.contrib import admin
from django.contrib import messages

from django.db.models import Q, F
from django.db.models.functions import Lower

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import File

from tales_django.sites import unfold_admin_site

from core.ffmpeg import probeDuration
from core.helpers.errors import errorToString
from core.logging import getDebugLogger, errorStyle, warningTitleStyle, tretiaryStyle

from ..models import Track


_logger = getDebugLogger()


class IsPublishedFilter(admin.SimpleListFilter):
    """
    Published tracks filter
    """

    title = _('Published')
    parameter_name = 'is_published'

    def lookups(self, request, model_admin):
        return (
            ('1', _('True')),
            ('0', _('False')),
        )

    def queryset(self, _, queryset):
        if self.value() == '1':
            return queryset.filter(track_status='PUBLISHED')
        if self.value() == '0':
            return queryset.filter(~Q(track_status='PUBLISHED'))


@admin.action(description=_('Mark as published'))
def mark_published_action(modeladmin, request, queryset):
    queryset.update(track_status='PUBLISHED')


@admin.action(description=_('Mark as hidden'))
def mark_hidden_action(modeladmin, request, queryset):
    queryset.update(track_status='HIDDEN')


@admin.action(description=_('Mark as test'))
def mark_test_action(modeladmin, request, queryset):
    queryset.update(track_status='TEST')


@admin.action(description=_('Promote'))
def promote_action(modeladmin, request, queryset):
    queryset.update(promote=True)


@admin.action(description=_('No promote'))
def no_promote_action(modeladmin, request, queryset):
    queryset.update(promote=False)


@admin.register(Track, site=unfold_admin_site)
class TrackAdmin(TranslatedFieldAdmin, ImportExportModelAdmin, ExportActionModelAdmin, UnfoldModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm

    fieldsets = (
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
            _('Description'),
            {
                'fields': (
                    'description_ru',
                    'description_en',
                )
            },
        ),
        (
            _('Media'),
            {
                'fields': (
                    # 'youtube_url',
                    'audio_file',
                    'preview_picture',
                )
            },
        ),
        (
            _('Attributes'),
            {
                'fields': (
                    'author',
                    'tags',
                    'rubrics',
                )
            },
        ),
        (
            _('Status'),
            {
                'fields': (
                    'track_status',
                    'promote',
                    'for_members',
                )
            },
        ),
        (
            _('Publication'),
            {
                'fields': (
                    'published_at',
                    'published_by',
                )
            },
        ),
        (
            _('Information'),
            {
                'fields': (
                    'played_count',
                    # 'audio_duration',
                    # 'audio_size',
                    'duration_formatted',
                    'size_formatted',
                    # 'updated_at',
                    # 'updated_by',
                )
            },
        ),
    )

    actions = [
        mark_published_action,
        mark_hidden_action,
        mark_test_action,
        promote_action,
        no_promote_action,
    ]
    list_display = [
        'title_translated',
        'author',
        'rubrics_list',
        'tags_list',
        'duration_formatted',
        'size_formatted',
        'promote',
        'is_published',
        'published_at',
        'updated_at',
        # 'published_by',
        # 'has_preview',
        # 'for_members',
    ]
    search_fields = [
        'title_en',
        'title_ru',
    ]
    readonly_fields = (
        'duration_formatted',
        'size_formatted',
        'played_count',
        # 'audio_duration',
        # 'audio_size',
        # 'published_at',
        # 'published_by',
        # 'updated_at',
        # 'updated_by',
    )
    exclude = (
        # 'published_by',
        # 'published_at',
        # 'updated_by',
        # 'updated_at',
        'audio_duration',
        'audio_size',
    )
    list_filter = [
        IsPublishedFilter,
        'track_status',
        'promote',
        'published_at',
        'updated_at',
        'author',
        'rubrics',
        'tags',
        # 'played_count',
    ]

    IsPublishedFilter.boolean = True

    def is_published(self, track):
        return track.track_status == 'PUBLISHED'

    is_published.admin_order_field = 'track_status'

    is_published.short_description = _('Published')
    is_published.boolean = True

    def has_preview(self, track):
        return True if track.preview_picture else False

    has_preview.admin_order_field = 'preview_picture'

    has_preview.short_description = _('Has preview')
    has_preview.boolean = True

    def tags_list(self, track):
        tagNames = map(lambda t: t.text, track.tags.all())
        return ', '.join(tagNames)

    tags_list.short_description = _('Tags')

    def rubrics_list(self, track):
        rubricNames = map(lambda t: t.text, track.rubrics.all())
        return ', '.join(rubricNames)

    rubrics_list.short_description = _('Rubrics')

    def duration_formatted(self, track):
        return track.duration_formatted

    duration_formatted.admin_order_field = 'audio_duration'

    duration_formatted.short_description = _('Duration')

    def size_formatted(self, track):
        return track.size_formatted   # sizeofFmt(track.audio_size) if track.audio_size else '-'

    size_formatted.admin_order_field = 'audio_size'

    size_formatted.short_description = _('Size')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _title_translated=F('title_' + get_language()),
        )
        return queryset

    def title_translated(self, track):
        return track.title

    title_translated.admin_order_field = Lower('_title_translated')
    title_translated.short_description = _('Title')

    def get_ordering(self, request):
        return [
            '-published_at',
            Lower(to_attribute('title')),
        ]

    def get_changeform_initial_data(self, request):
        get_data = super(TrackAdmin, self).get_changeform_initial_data(request)
        # Set creator user
        get_data['published_by'] = request.user.id
        return get_data

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):
        """
        Auto update owning users
        """
        # Update updater info...
        obj.updated_by_id = request.user.id
        # Get audio duration
        audioFile = obj.audio_file
        fileInstance: File | TemporaryUploadedFile = audioFile.file
        if fileInstance and isinstance(fileInstance, TemporaryUploadedFile):
            try:
                obj.audio_size = audioFile.size
                # Trying to determine audio track length
                tempFile = fileInstance.file
                tempFilePath = tempFile.name
                duration = probeDuration(tempFilePath)
                if not duration:
                    raise Exception('Can not determine correct audio duration.')
                obj.audio_duration = duration
                sizeFmt = self.size_formatted(obj)
                durationFmt = self.duration_formatted(obj)
                # Translate...
                msgData = {'sizeFmt': sizeFmt, 'durationFmt': durationFmt}
                msgTmpl = _(
                    'Audio file has been successfully uploaded'
                    # 'Audio file has been successfully uploaded and its data updated: size is %(sizeFmt)s, duration is %(durationFmt)s'
                )
                msgText = msgTmpl % msgData
                messages.add_message(request, messages.SUCCESS, msgText)
            except Exception as err:
                errText = errorToString(err, show_stacktrace=False)
                sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
                errMsg = 'Error probing an audio: ' + errText
                _logger.info(
                    warningTitleStyle('save_model: Traceback for the following error:') + tretiaryStyle(sTraceback)
                )
                _logger.error(errorStyle('save_model: ' + errMsg))
                messages.add_message(request, messages.ERROR, errMsg)
                obj.track_status = 'HIDDEN'
                obj.audio_duration = None
                # TODO: Prevent leaving the edit page?
        return super().save_model(request, obj, form, change)
