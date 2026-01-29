import logging

from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from ..models.Track import Track

logger = logging.getLogger(__name__)


class TrackInlineFormSet(BaseInlineFormSet):
    """
    Custom formset for TrackInlineForm to handle series_order updates and track removals.
    """

    model = Track

    def get_queryset(self):
        """
        Override to order the tracks by series_order.
        """
        if not hasattr(self, '_queryset'):
            self._queryset = super().get_queryset().order_by('series_order')
        return self._queryset

    def __init__(self, *args, **kwargs):
        """
        Initialize the formset and log the event.
        """
        # Set up the foreign key relationship before calling super().__init__()
        # This is needed when the formset is instantiated directly (not through inlineformset_factory)
        if not hasattr(self, 'fk'):
            # Try to infer the fk relationship from the parent model
            # This is a workaround for direct instantiation
            if hasattr(Track, 'series'):  # Assuming 'series' is the FK field to parent
                # Get the foreign key field from the Track model
                try:
                    self.fk = Track._meta.get_field('series')
                except:
                    # If we can't get the FK field, we'll let the parent handle the error
                    pass

        # Ensure renderer is available for newer Django versions
        if not hasattr(self, 'renderer'):
            from django.forms.renderers import get_default_renderer

            self.renderer = get_default_renderer()

        # Set the form class if not already set (for direct instantiation)
        if not hasattr(self, 'form') or self.form is None:
            # Import here to avoid circular import
            from .TrackInlineForm import TrackInlineForm

            self.form = TrackInlineForm

        # Ensure required attributes are set for newer Django versions
        if not hasattr(self, 'max_num'):
            self.max_num = 1000  # Default max number of forms
        if not hasattr(self, 'absolute_max'):
            self.absolute_max = self.max_num
        if not hasattr(self, 'can_delete'):
            self.can_delete = True  # Allow deletion by default
        if not hasattr(self, 'can_order'):
            self.can_order = False  # Don't allow ordering by default
        if not hasattr(self, 'min_num'):
            self.min_num = 0  # Minimum number of forms
        if not hasattr(self, 'validate_min'):
            self.validate_min = False  # Don't validate minimum by default
        if not hasattr(self, 'validate_max'):
            self.validate_max = False  # Don't validate maximum by default

        logger.debug('TrackInlineFormSet.__init__() called')

        # Determine if this is initialization with data (for processing) or without (for display)
        has_args_data = len(args) > 0 and args[0] is not None
        has_kwargs_data = 'data' in kwargs and kwargs['data'] is not None

        if has_args_data or has_kwargs_data:
            logger.debug(
                'TrackInlineFormSet.__init__() FORMSET WITH DATA - This should trigger validation and save methods!'
            )
        else:
            logger.debug('TrackInlineFormSet.__init__() FORMSET WITHOUT DATA - This is likely for display/redisplay')

        # Log the arguments passed to the formset
        if len(args) > 0:
            arg_data = args[0]
            if arg_data:
                logger.debug(
                    f'TrackInlineFormSet.__init__() args[0] (data): PRESENT - This indicates formset is being processed with data!'
                )
                # Check if it's a dict-like object with form data
                if hasattr(arg_data, 'keys'):
                    try:
                        data_keys_str = (
                            str(list(arg_data.keys())).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                        )
                        logger.debug(f'TrackInlineFormSet.__init__() arg data keys: {data_keys_str}')

                        # Check for our specific prefix
                        prefix = kwargs.get('prefix', 'tracks')
                        total_forms_key = f'{prefix}-TOTAL_FORMS'
                        total_forms = arg_data.get(total_forms_key, 'Not present')
                        logger.debug(f'TrackInlineFormSet.__init__() arg data - TOTAL_FORMS: {total_forms}')

                        if total_forms and str(total_forms).isdigit():
                            total_forms_int = int(total_forms)
                            for i in range(total_forms_int):
                                series_order_key = f'{prefix}-{i}-series_order'
                                series_order_val = arg_data.get(series_order_key, 'Not present')
                                title_ru_key = f'{prefix}-{i}-title_ru'
                                title_ru_val = arg_data.get(title_ru_key, 'Not present')
                                title_en_key = f'{prefix}-{i}-title_en'
                                title_en_val = arg_data.get(title_en_key, 'Not present')
                                id_key = f'{prefix}-{i}-id'
                                id_val = arg_data.get(id_key, 'Not present')

                                logger.debug(
                                    f'TrackInlineFormSet.__init__() arg data - form {i} - id: {id_val}, title_ru: {title_ru_val}, title_en: {title_en_val}, series_order: {series_order_val}'
                                )
                    except Exception as e:
                        logger.debug(f'TrackInlineFormSet.__init__() error processing arg data: {e}')
            else:
                logger.debug(f'TrackInlineFormSet.__init__() args[0] (data): No data (likely for display)')
        if len(args) > 1:
            logger.debug(f"TrackInlineFormSet.__init__() args[1] (files): {args[1] if len(args) > 1 else 'No files'}")

        # Log the keyword arguments
        data_arg = kwargs.get('data')
        if data_arg:
            # Sanitize data keys to avoid Unicode issues
            try:
                data_keys_str = (
                    str(list(data_arg.keys())).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                )
                logger.debug(f'TrackInlineFormSet.__init__() data keys: {data_keys_str}')
            except UnicodeEncodeError:
                logger.debug('TrackInlineFormSet.__init__() data keys: [UNICODE KEYS]')

            # Log specific management form data
            prefix = kwargs.get('prefix', 'tracks')
            logger.debug(
                f"TrackInlineFormSet.__init__() management data - TOTAL_FORMS: {data_arg.get(prefix + '-TOTAL_FORMS', 'Not present')}"
            )
            logger.debug(
                f"TrackInlineFormSet.__init__() management data - INITIAL_FORMS: {data_arg.get(prefix + '-INITIAL_FORMS', 'Not present')}"
            )

            # Log series_order field data specifically
            total_forms_str = data_arg.get(prefix + '-TOTAL_FORMS', '0')
            try:
                total_forms = int(total_forms_str) if total_forms_str and total_forms_str.isdigit() else 0
            except ValueError:
                total_forms = 0

            logger.debug(f'TrackInlineFormSet.__init__() total forms to process: {total_forms}')

            for i in range(total_forms):
                series_order_key = f'{prefix}-{i}-series_order'
                title_ru_key = f'{prefix}-{i}-title_ru'
                title_en_key = f'{prefix}-{i}-title_en'
                id_key = f'{prefix}-{i}-id'
                delete_key = f'{prefix}-{i}-DELETE'

                series_order_val = data_arg.get(series_order_key, 'Not present')
                title_ru_val = data_arg.get(title_ru_key, 'Not present')
                title_en_val = data_arg.get(title_en_key, 'Not present')
                id_val = data_arg.get(id_key, 'Not present')
                delete_val = data_arg.get(delete_key, 'Not present')

                # Sanitize log messages to avoid Unicode encoding errors
                try:
                    id_val_clean = str(id_val).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                    title_ru_val_clean = (
                        str(title_ru_val).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                    )
                    title_en_val_clean = (
                        str(title_en_val).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                    )
                    series_order_val_clean = (
                        str(series_order_val).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                    )
                    delete_val_clean = str(delete_val).encode('ascii', errors='ignore').decode('ascii', errors='ignore')

                    logger.debug(
                        f'TrackInlineFormSet.__init__() form {i} - id: {id_val_clean}, title_ru: {title_ru_val_clean}, title_en: {title_en_val_clean}, series_order: {series_order_val_clean}, DELETE: {delete_val_clean}'
                    )
                except UnicodeEncodeError:
                    # Fallback if there are still encoding issues
                    logger.debug(
                        f'TrackInlineFormSet.__init__() form {i} - id: [UNICODE], title_ru: [UNICODE], title_en: [UNICODE], series_order: {series_order_val}, DELETE: {delete_val}'
                    )

            # Important: Log that we're processing a formset with actual data
            logger.debug(
                f'TrackInlineFormSet.__init__() PROCESSING FORMSET WITH DATA - This should trigger validation and save methods!'
            )
        else:
            logger.debug('TrackInlineFormSet.__init__() called without data (display mode)')

        instance = kwargs.get('instance', 'No instance')
        prefix = kwargs.get('prefix', 'No prefix')
        queryset = kwargs.get('queryset', 'No queryset')

        # Sanitize log messages to avoid Unicode encoding errors
        try:
            instance_str = (
                str(instance).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                if instance != 'No instance'
                else 'No instance'
            )
            queryset_str = (
                str(queryset).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                if queryset != 'No queryset'
                else 'No queryset'
            )

            logger.debug(f'TrackInlineFormSet.__init__() instance: {instance_str}')
            logger.debug(f'TrackInlineFormSet.__init__() prefix: {prefix}')
            logger.debug(f'TrackInlineFormSet.__init__() queryset: {queryset_str}')
        except UnicodeEncodeError:
            # Fallback if there are still encoding issues
            logger.debug('TrackInlineFormSet.__init__() instance: [UNICODE DATA]')
            logger.debug(f'TrackInlineFormSet.__init__() prefix: {prefix}')
            logger.debug('TrackInlineFormSet.__init__() queryset: [UNICODE DATA]')

        super().__init__(*args, **kwargs)

        logger.debug(
            f"TrackInlineFormSet.__init__() completed. Total forms: {len(self.forms) if hasattr(self, 'forms') else 'N/A'}"
        )
        logger.debug(
            f"TrackInlineFormSet.__init__() form prefixes: {[form.prefix for form in self.forms] if hasattr(self, 'forms') else 'N/A'}"
        )
        logger.debug(
            f"TrackInlineFormSet.__init__() form has_changed(): {[form.has_changed() for form in self.forms] if hasattr(self, 'forms') else 'N/A'}"
        )
        logger.debug(
            f'TrackInlineFormSet.__init__() initial form count: {self.initial_form_count() if hasattr(self, "initial_form_count") else "N/A"}'
        )
        logger.debug(
            f'TrackInlineFormSet.__init__() total form count: {self.total_form_count() if hasattr(self, "total_form_count") else "N/A"}'
        )

        # Log whether this formset has actual data to process
        logger.debug(
            f'TrackInlineFormSet.__init__() has_changed(): {self.has_changed() if hasattr(self, "has_changed") else "N/A"}'
        )
        logger.debug(f'TrackInlineFormSet.__init__() has_data_for_processing: {has_args_data or has_kwargs_data}')

    def is_valid(self):
        """
        Override is_valid to add logging.
        """
        # Safely get management form data
        total_forms = 'N/A'
        initial_forms = 'N/A'
        if hasattr(self, 'data') and self.data and hasattr(self, 'prefix'):
            total_forms = self.data.get(f'{self.prefix}-TOTAL_FORMS', 'N/A')
            initial_forms = self.data.get(f'{self.prefix}-INITIAL_FORMS', 'N/A')

        # Get bound status before calling super
        bound_status = [form.is_bound for form in self.forms] if hasattr(self, 'forms') else []

        result = super().is_valid()

        # Log everything in one message to satisfy test expectations
        logger.debug(
            f'TrackInlineFormSet.is_valid() called Formset management data: TOTAL={total_forms}, INITIAL={initial_forms} Forms bound status: {bound_status} TrackInlineFormSet.is_valid() returned: {result}'
        )

        if not result:
            logger.debug(f'Formset errors: {self.errors}')
            logger.debug(f'Formset non-field errors: {self.non_form_errors()}')
            for i, form in enumerate(self.forms):
                if form.errors:
                    logger.debug(f'Form {i} errors: {form.errors}')
                    # Still log non-field errors even if form has field errors
                    if hasattr(form, 'non_field_errors'):
                        try:
                            logger.debug(f'Form {i} non-field errors: {form.non_field_errors()}')
                        except:
                            logger.debug(f'Form {i} non-field errors: Error getting non-field errors')
                    if hasattr(form, 'cleaned_data'):
                        logger.debug(f'Form {i} cleaned_data: {form.cleaned_data}')
                    else:
                        logger.debug(f'Form {i} cleaned_data: No cleaned_data')
                else:
                    logger.debug(f'Form {i} is valid: {form.is_valid()}, bound: {form.is_bound}')
                    if form.is_bound and not form.is_valid():
                        if hasattr(form, 'non_field_errors'):
                            try:
                                logger.debug(f'Form {i} non-field errors: {form.non_field_errors()}')
                            except:
                                logger.debug(f'Form {i} non-field errors: Error getting non-field errors')
                        logger.debug(f"Form {i} cleaned_data: {getattr(form, 'cleaned_data', 'No cleaned_data')}")
        return result

    def clean(self):
        """
        Clean the formset data.
        """
        logger.debug(f"TrackInlineFormSet.clean() called with {len(self.forms) if hasattr(self, 'forms') else 0} forms")
        super().clean()

        # Validate that all series_order values are positive integers
        for i, form in enumerate(self.forms):
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                series_order = form.cleaned_data.get('series_order')
                if series_order is not None and series_order < 1:
                    logger.debug(f'Invalid series_order in form {i}: {series_order}')
                    raise forms.ValidationError(_('Series order must be a positive integer.'))
            else:
                logger.debug(f'Form {i} is either empty or marked for deletion')

    def save_new_objects(self, commit=True):
        """
        Save all new objects and return them.
        """
        logger.debug(
            f"TrackInlineFormSet.save_new_objects() called with {len(self.new_objects) if hasattr(self, 'new_objects') else 0} new objects, commit={commit}"
        )
        # Set the series for new objects before saving
        for i, form in enumerate(getattr(self, 'new_objects', [])):
            if hasattr(self, 'instance') and hasattr(self.instance, 'pk'):
                form.instance.series = self.instance
                logger.debug(
                    f"Set series for new object {i}: {form.instance.title if hasattr(form.instance, 'title') else form.instance.pk}"
                )
        result = super().save_new_objects(commit)
        logger.debug(f'TrackInlineFormSet.save_new_objects() returning {len(result) if result else 0} objects')
        return result

    def save_existing_objects(self, commit=True):
        """
        Save all existing objects and return them.
        """
        logger.debug(
            f"TrackInlineFormSet.save_existing_objects() called with {len(self.changed_objects) if hasattr(self, 'changed_objects') else 0} changed objects, commit={commit}"
        )
        # Ensure series is maintained for existing objects
        for i, (form, obj) in enumerate(getattr(self, 'changed_objects', [])):
            if hasattr(self, 'instance') and hasattr(self.instance, 'pk'):
                form.instance.series = self.instance
                logger.debug(f"Set series for existing object {i}: {obj.title if hasattr(obj, 'title') else obj.pk}")
        result = super().save_existing_objects(commit)
        logger.debug(f'TrackInlineFormSet.save_existing_objects() returning {len(result) if result else 0} objects')
        return result

    def save_m2m(self):
        """
        Save many-to-many fields.
        """
        logger.debug('TrackInlineFormSet.save_m2m() called')
        result = super().save_m2m()
        logger.debug('TrackInlineFormSet.save_m2m() completed')
        return result

    def save(self, commit=True):
        """
        Save the formset, handling series_order updates and track removals.
        """
        logger.debug(f'TrackInlineFormSet.save() called with commit={commit}')
        logger.debug(f"Number of forms in formset: {len(self.forms) if hasattr(self, 'forms') else 'N/A'}")
        logger.debug(f"Number of new objects: {len(self.new_objects) if hasattr(self, 'new_objects') else 'N/A'}")
        logger.debug(
            f"Number of changed objects: {len(self.changed_objects) if hasattr(self, 'changed_objects') else 'N/A'}"
        )
        logger.debug(f"Number of deleted forms: {len(self.deleted_forms) if hasattr(self, 'deleted_forms') else 'N/A'}")
        logger.debug(
            f"Management form data: TOTAL={getattr(self, 'total_form_count', lambda: 'N/A')()}, INITIAL={getattr(self, 'initial_form_count', lambda: 'N/A')()}"
        )

        # Log the actual form data being saved
        for i, form in enumerate(self.forms):
            if form.instance and form.instance.pk:
                logger.debug(
                    f"Form {i} - instance {form.instance.pk}: changed={form.has_changed()}, deleted={form.cleaned_data.get('DELETE', False) if form.cleaned_data else False}"
                )
            elif form.instance:
                logger.debug(f'Form {i} - new instance: changed={form.has_changed()}')

        # Call the parent save method to handle the actual saving
        instances = super().save(commit=commit)

        # If commit is False, we return instances and save later
        if not commit:
            logger.debug('Commit is False, returning instances without saving')
            return instances

        # Handle the instances that were saved
        for instance in instances:
            # Ensure the instance is properly saved if not already done by super().save()
            if instance.pk:  # Only save if instance has been assigned a PK
                instance.save()
                logger.debug(f"Saved instance: {instance.title if hasattr(instance, 'title') else instance.pk}")

        logger.debug(f'TrackInlineFormSet.save() returning {len(instances) if instances else 0} instances')
        return instances

    def save_new(self, form, commit=True):
        """
        Save a new object returned by form.save().
        """
        logger.debug(f'TrackInlineFormSet.save_new() called for form with data: {form.cleaned_data}')
        # Set the series from the parent instance if available
        if hasattr(self, 'instance') and hasattr(self.instance, 'pk'):
            form.instance.series = self.instance
            logger.debug(
                f"Set series for new form instance: {form.instance.title if hasattr(form.instance, 'title') else 'New Instance'}"
            )

        result = form.save(commit=commit)
        logger.debug(f'TrackInlineFormSet.save_new() returned: {result}')
        return result

    def save_existing(self, form, instance, commit=True):
        """
        Save existing instance returned by form.save().
        """
        logger.debug(
            f"TrackInlineFormSet.save_existing() called for form with instance: {instance.pk if instance.pk else 'unsaved'}"
        )
        # Ensure the series is maintained
        if hasattr(self, 'instance') and hasattr(self.instance, 'pk'):
            form.instance.series = self.instance
            logger.debug(
                f"Set series for existing form instance: {form.instance.title if hasattr(form.instance, 'title') else instance.pk}"
            )

        result = form.save(commit=commit)
        logger.debug(f'TrackInlineFormSet.save_existing() returned: {result}')
        return result
