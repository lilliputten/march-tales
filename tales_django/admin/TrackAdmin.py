from datetime import timedelta
import traceback
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.contrib import messages

# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.files.base import File
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile

from core.ffmpeg import probeDuration
from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString
from core.logging import getDebugLogger, errorStyle, warningTitleStyle
from core.logging.utils import tretiaryStyle

from ..models import Track
from ..forms import TrackAdminForm


_logger = getDebugLogger()


class IsPublishedFilter(SimpleListFilter):
    """
    Published tracks filter
    """

    title = 'Published'
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


class TrackAdmin(admin.ModelAdmin):
    form = TrackAdminForm
    list_display = [
        'title',
        'duration_formated',
        'size_formated',
        # 'resolved_date',
        'created_at',
        'created_by',
        'has_preview',
        'is_published',
    ]
    readonly_fields = (
        'duration_formated',
        'size_formated',
        # 'audio_duration',
        # 'audio_size',
        # 'created_at',
        # 'created_by',
        # 'updated_at',
        # 'updated_by',
    )
    exclude = (
        # 'created_by',
        'updated_by',
        # 'created_at',
        'updated_at',
        'audio_duration',
        'audio_size',
    )
    list_filter = [
        IsPublishedFilter,
    ]

    def is_published(self, track):
        return track.track_status == 'PUBLISHED'

    is_published.short_description = 'Published'
    is_published.boolean = True

    def has_preview(self, track):
        return True if track.preview_picture else False

    has_preview.short_description = 'Has preview'
    has_preview.boolean = True

    # def resolved_date(self, track):
    #     return track.date if track.date else track.created_at
    # resolved_date.short_description = 'Date'

    def duration_formated(self, track):
        return str(timedelta(seconds=track.audio_duration)) if track.audio_duration else '-'

    duration_formated.short_description = 'Duration'

    def size_formated(self, track):
        return sizeofFmt(track.audio_size) if track.audio_size else '-'

    size_formated.short_description = 'Size'

    def get_changeform_initial_data(self, request):
        get_data = super(TrackAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
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
        # if not obj.created_by_id:
        #     obj.created_by_id = request.user.id
        # Update user...
        obj.updated_by_id = request.user.id
        # Get audio duration
        audioFile = obj.audio_file
        # fileObj: File | InMemoryUploadedFile = audioFile.file # File | InMemoryUploadedFile
        try:
            obj.audio_size = audioFile.size
            # Trying to determine audio track length
            tempFile = audioFile.file.file
            tempFilePath = tempFile.name
            duration = probeDuration(tempFilePath)
            obj.audio_duration = round(duration)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error probing an audio: ' + errText
            _logger.info(
                warningTitleStyle('save_model: Traceback for the following error:') + tretiaryStyle(sTraceback)
            )
            _logger.error(errorStyle('save_model: ' + errMsg))
            messages.add_message(request, messages.ERROR, errMsg)
        # messages.add_message(request, messages.SUCCESS, 'Add audio track of length %d' % duration)
        super().save_model(request, obj, form, change)


admin.site.register(Track, TrackAdmin)
