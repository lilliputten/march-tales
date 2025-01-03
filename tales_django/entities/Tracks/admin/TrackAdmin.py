from datetime import timedelta
import traceback
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.contrib import messages

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import File

# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile

from core.ffmpeg import probeDuration
from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString
from core.logging import getDebugLogger, errorStyle, warningTitleStyle, tretiaryStyle

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


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    form = TrackAdminForm
    list_display = [
        'title',
        'author',
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

    def is_published(self, track):
        return track.track_status == 'PUBLISHED'

    is_published.admin_order_field = 'track_status'

    is_published.short_description = 'Published'
    is_published.boolean = True

    def has_preview(self, track):
        return True if track.preview_picture else False

    has_preview.admin_order_field = 'preview_picture'

    has_preview.short_description = 'Has preview'
    has_preview.boolean = True

    def tags_list(self, track):
        tagNames = map(lambda t: t.text, track.tags.all())
        return ', '.join(tagNames)

    tags_list.short_description = 'Tags'

    # def resolved_date(self, track):
    #     return track.date if track.date else track.published_at
    # resolved_date.short_description = 'Date'

    def duration_formatted(self, track):
        return (
            track.duration_formatted
        )   # str(timedelta(seconds=track.audio_duration)) if track.audio_duration else '-'

    duration_formatted.admin_order_field = 'audio_duration'

    duration_formatted.short_description = 'Duration'

    def size_formatted(self, track):
        return track.size_formatted   # sizeofFmt(track.audio_size) if track.audio_size else '-'

    size_formatted.admin_order_field = 'audio_size'

    size_formatted.short_description = 'Size'

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
                obj.audio_duration = round(duration)
                sizeFmt = self.size_formatted(obj)
                durationFmt = self.duration_formatted(obj)
                msgText = f'Audio has been successfully uploaded and its data updated: size is {sizeFmt}, duration is {durationFmt}'
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
