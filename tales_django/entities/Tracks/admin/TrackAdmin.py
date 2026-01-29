import traceback

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import CharField, F, Max, Q, Value
from django.db.models.functions import Concat, Lower
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from translated_fields import TranslatedFieldAdmin, to_attribute
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm  # , SelectableFieldsExportForm

from core.ffmpeg import probeDuration
from core.helpers.errors import errorToString
from core.helpers.files import sizeofFmt
from core.logging import errorStyle, getDebugLogger, tretiaryStyle, warningTitleStyle
from tales_django.sites import unfold_admin_site

from ..forms.TrackAdminForm import TrackAdminForm
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


class HasSeriesFilter(admin.SimpleListFilter):
    """
    Filter tracks by whether they belong to a series
    """

    title = _('Has Series')
    parameter_name = 'has_series'

    def lookups(self, request, model_admin):
        return (
            ('1', _('True')),
            ('0', _('False')),
        )

    def queryset(self, _, queryset):
        if self.value() == '1':
            return queryset.filter(series__isnull=False)
        if self.value() == '0':
            return queryset.filter(series__isnull=True)


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
class TrackAdmin(
    TranslatedFieldAdmin,
    ImportExportModelAdmin,
    ExportActionModelAdmin,
    UnfoldModelAdmin,
):
    form = TrackAdminForm
    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        (
            _('Title'),
            {
                'classes': ['--collapse', '--opened-by-default', 'columns'],
                'fields': (
                    'title_ru',
                    'title_en',
                ),
            },
        ),
        (
            _('Description'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'description_ru',
                    'description_en',
                ),
            },
        ),
        (
            _('Media'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    # 'youtube_url',
                    'audio_file',
                    'preview_picture',
                ),
            },
        ),
        (
            _('Attributes'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'author',
                    'tags',
                    'rubrics',
                ),
            },
        ),
        (
            _('Series'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'series',
                    'series_order',
                ),
            },
        ),
        (
            _('Status'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'track_status',
                    'promote',
                    'for_members',
                ),
            },
        ),
        (
            _('Updates'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'published_at',
                    'published_by',
                    'updated_at',
                    'updated_by',
                ),
            },
        ),
        (
            _('Information'),
            {
                'classes': ['--collapse', 'columns'],
                'fields': (
                    'played_count',
                    # 'audio_duration',
                    # 'audio_size',
                    'duration_formatted',
                    'size_formatted',
                ),
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
        'series_title_only',
        'series_order',
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
        'updated_at',
        'updated_by',
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
        HasSeriesFilter,
        'track_status',
        'promote',
        'published_at',
        'updated_at',
        'series',
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

    def series_title_only(self, track):
        # Get the series title only if series exists
        if track.series:
            return track.series.title
        return '-'

    series_title_only.admin_order_field = '_series_title'  # Use annotated field for sorting
    series_title_only.short_description = _('Series')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('series')
        language = get_language()
        queryset = queryset.annotate(
            _title_translated=F(f'title_{language}'),
            # Handle potential null series for sorting
            _series_title=F(f'series__title_{language}'),
            # Add series_order to the queryset for sorting
            _series_order=F('series_order'),
        )
        return queryset

    def duration_formatted(self, track):
        return track.duration_formatted

    duration_formatted.admin_order_field = 'audio_duration'

    duration_formatted.short_description = _('Duration')

    def size_formatted(self, track):
        return sizeofFmt(track.audio_size) if track.audio_size else '-'

    size_formatted.admin_order_field = 'audio_size'

    size_formatted.short_description = _('Size')

    def title_translated(self, track):
        return track.title

    title_translated.admin_order_field = Lower('_title_translated')
    title_translated.short_description = _('Title')

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
        Create/validate series_order fields and uploaded process audio file information.

        This method executes automatically when saving a Track model instance, with main functions including:
        1. Auto-set or validate track order within a series
        2. Update last modifier information
        3. Process audio file duration and size information

        Args:
            request: Django HTTP request object
            obj: Track model instance to be saved
            form: Form object containing form data
            change: Boolean indicating if this is an update to an existing record

        Returns:
            None: Calls parent class's save_model method to complete actual saving operation
        """

        # NOTE: The data preparing and verification is proceeded in the
        # `tales_django/entities/Tracks/forms/TrackAdminForm.py`. It's just a
        # reassuring here.
        if obj.series:
            # Auto-set series_order if series is set but series_order is not provided
            if obj.series_order is None or obj.series_order == '' or obj.series_order == 0:
                # Find the highest series_order in the series and add 1
                max_order = obj.series.tracks.aggregate(max_order=Max('series_order'))['max_order']
                obj.series_order = (max_order or 0) + 1

            # Check if series_order is unique within the series
            elif obj.series_order:
                # Find other tracks in the same series with the same series_order
                same_order_tracks = Track.objects.filter(series=obj.series, series_order=obj.series_order)

                # If updating an existing track, exclude it from the check
                if obj.pk:
                    same_order_tracks = same_order_tracks.exclude(pk=obj.pk)

                if same_order_tracks.exists():
                    # Add an error message to the request
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f'Track order {obj.series_order} already exists in series {obj.series.title}. '
                        f'Each track in a series must have a unique order number.',
                    )
                    return  # Skip saving if there's a duplicate series_order

        # Update updater info...
        obj.updated_by_id = request.user.id
        # Get audio duration
        audioFile = obj.audio_file
        fileInstance: File | TemporaryUploadedFile = None
        try:
            fileInstance = audioFile.file
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Can not access an audio file: ' + errText
            _logger.info(
                warningTitleStyle('save_model: Traceback for the following error:') + tretiaryStyle(sTraceback)
            )
            _logger.error(errorStyle('save_model: ' + errMsg))
            messages.add_message(request, messages.ERROR, errMsg)
            obj.track_status = 'HIDDEN'
            obj.audio_duration = None
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

    # def save_form_m2m(self, request, form, formsets, change):
    #     """Save M2M relationships."""
    #     # Save the M2M relationships
    #     return super().save_form_m2m(request, form, formsets, change)

    #     # # Validate unique series_order since M2M relationships are established
    #     # try:
    #     #     obj.validate_unique_series_order()
    #     # except ValidationError as e:
    #     #     # If validation fails, add error message
    #     #     messages.add_message(request, messages.ERROR, e.message)
    #     #     # Note: At this point, M2M relationships are already saved
    #     #     # In a production system, you might want to implement transaction rollback
