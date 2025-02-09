import traceback

from translated_fields import TranslatedFieldAdmin, to_attribute

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, F
from django.db.models.functions import Lower

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import File

from core.ffmpeg import probeDuration
from core.helpers.errors import errorToString
from core.logging import getDebugLogger, errorStyle, warningTitleStyle, tretiaryStyle

from ..models import Track
from ..forms import TrackAdminForm


_logger = getDebugLogger()


class IsPublishedFilter(SimpleListFilter):
    """
    Published tracks filter
    """

    title = _('Published')
    parameter_name = 'is_published'

    def lookups(self, _, __):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, _, queryset):
        if self.value() == '1':
            return queryset.filter(track_status='PUBLISHED')
        if self.value() == '0':
            return queryset.filter(~Q(track_status='PUBLISHED'))


@admin.register(Track)
class TrackAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    form = TrackAdminForm
    list_display = [
        'title_translated',
        'author',
        'rubrics_list',
        'tags_list',
        'duration_formatted',
        'size_formatted',
        # 'resolved_date',
        'published_at',
        'published_by',
        'has_preview',
        'for_members',
        'is_published',
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
        'updated_by',
        # 'published_at',
        'updated_at',
        'audio_duration',
        'audio_size',
    )
    list_filter = [
        IsPublishedFilter,
    ]

    # fieldsets = [
    #     (_('title'), {'fields': Track.title.fields}),
    #     (_('description'), {'fields': Track.description.fields}),
    # ]

    def is_published(self, track):
        return track.track_status == 'PUBLISHED'

    is_published.admin_order_field = 'track_status'

    is_published.short_description = _('Published')
    is_published.boolean = True

    def has_preview(self, track):
        return True if track.preview_picture else False

    has_preview.admin_order_field = 'preview_picture'

    has_preview.short_description = _('has preview')
    has_preview.boolean = True

    def tags_list(self, track):
        tagNames = map(lambda t: t.text, track.tags.all())
        return ', '.join(tagNames)

    tags_list.short_description = _('tags')

    def rubrics_list(self, track):
        rubricNames = map(lambda t: t.text, track.rubrics.all())
        return ', '.join(rubricNames)

    rubrics_list.short_description = _('rubrics')

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
    title_translated.short_description = _('title')

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
