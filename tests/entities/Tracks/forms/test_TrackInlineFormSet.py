from unittest.mock import Mock, patch

from django.forms import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.test import TestCase

from tales_django.entities.Tracks.forms.TrackInlineFormSet import TrackInlineFormSet
from tales_django.entities.Tracks.models import Series, Track


class TrackInlineFormSetTestCase(TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create the formset class using inlineformset_factory to properly initialize
        self.TrackFormSet = inlineformset_factory(
            Series,  # Parent model
            Track,  # Child model
            formset=TrackInlineFormSet,
            fields=('id', 'title_ru', 'title_en', 'series_order'),  # Match the fields from the admin
            extra=0,
            can_delete=True,
        )

        # Create an instance for testing
        self.mock_formset = self.TrackFormSet()
        # Mock formset forms for consistent testing
        self.mock_formset.forms = [
            Mock(is_bound=True, is_valid=lambda: True, errors={}, cleaned_data={'name': 'Test Track'}),
            Mock(is_bound=False, is_valid=lambda: False, errors={'field': ['error']}),
        ]

    def test_is_valid_returns_true(self):
        """Test is_valid returns True and logs correct information."""
        with patch.object(BaseInlineFormSet, 'is_valid', return_value=True):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                result = self.mock_formset.is_valid()

                # Assert result
                self.assertTrue(result)

                # Assert logs
                self.assertIn('TrackInlineFormSet.is_valid() called', cm.output[0])
                self.assertIn('Formset management data: TOTAL=N/A, INITIAL=N/A', cm.output[0])
                self.assertIn('Forms bound status: [True, False]', cm.output[0])
                self.assertIn('TrackInlineFormSet.is_valid() returned: True', cm.output[0])

    def test_is_valid_returns_false(self):
        """Test is_valid returns False and logs error information."""
        with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                result = self.mock_formset.is_valid()

                # Assert result
                self.assertFalse(result)

                # Assert error logs
                log_output = ' '.join(cm.output)
                self.assertIn('Formset errors:', log_output)
                self.assertIn('Formset non-field errors:', log_output)
                self.assertIn('Form 0 is valid: True, bound: True', log_output)
                self.assertIn("Form 1 errors: {'field': ['error']}", log_output)

    def test_is_valid_with_bound_forms(self):
        """Test is_valid correctly logs form bound status."""
        # Update form bound status
        self.mock_formset.forms = [
            Mock(is_bound=True, is_valid=lambda: True, errors={}),
            Mock(is_bound=True, is_valid=lambda: False, errors={'name': ['required']}),
        ]

        with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                self.mock_formset.is_valid()

                # Assert bound status logs
                log_output = ' '.join(cm.output)
                self.assertIn('Forms bound status: [True, True]', log_output)
                self.assertIn('Form 1 non-field errors:', log_output)
                self.assertNotIn(
                    'Form 1 cleaned_data: No cleaned_data', log_output
                )  # Should not appear if form has errors

    def test_is_valid_with_unbound_forms(self):
        """Test is_valid handles unbound forms correctly."""
        # Update form bound status
        self.mock_formset.forms = [
            Mock(is_bound=False, is_valid=lambda: False, errors={}),
            Mock(is_bound=False, is_valid=lambda: False, errors={}),
        ]

        with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                self.mock_formset.is_valid()

                # Assert logs for unbound forms
                log_output = ' '.join(cm.output)
                self.assertIn('Forms bound status: [False, False]', log_output)
                self.assertIn('Form 0 is valid: False, bound: False', log_output)
                self.assertIn('Form 1 is valid: False, bound: False', log_output)

    def test_is_valid_with_management_data(self):

        # Create formset with management data in input
        data = {'test_prefix-TOTAL_FORMS': '5', 'test_prefix-INITIAL_FORMS': '2'}
        formset = self.TrackFormSet(data=data, files={}, prefix='test_prefix')
        formset.forms = [
            Mock(is_bound=True, is_valid=lambda: True, errors={}),
            Mock(is_bound=True, is_valid=lambda: True, errors={}),
            Mock(is_bound=False, is_valid=lambda: False, errors={}),
            Mock(is_bound=False, is_valid=lambda: False, errors={}),
        ]

        with patch.object(BaseInlineFormSet, 'is_valid', return_value=True):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                formset.is_valid()
        """Test is_valid logs formset-level non-field errors."""
        # Mock formset non-field errors
        self.mock_formset.non_form_errors = Mock(return_value=['Global validation error'])

        with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                self.mock_formset.is_valid()

                # Verify non-field errors logs
                log_output = ' '.join(cm.output)
                self.assertIn("Formset non-field errors: ['Global validation error']", log_output)

    def test_is_valid_with_bound_invalid_form_cleaned_data(self):
        """Test is_valid logs cleaned_data for bound invalid forms."""
        # Create form with bound status, invalid state, and cleaned_data
        form = Mock(
            is_bound=True,
            is_valid=lambda: False,
            errors={'duration': ['Invalid time format']},
            non_field_errors=Mock(return_value=['Form-level validation error']),
            cleaned_data={'title': 'Test Track', 'duration': '00:61:00'},
        )
        formset = TrackInlineFormSet(data={}, files={}, prefix='test_prefix')
        formset.forms = [form]

        with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
            with self.assertLogs('tales_django.entities.Tracks.forms.TrackInlineFormSet', level='DEBUG') as cm:
                formset.is_valid()

                # Verify cleaned_data logs
                log_output = ' '.join(cm.output)
                self.assertIn("Form 0 non-field errors: ['Form-level validation error']", log_output)
                self.assertIn("Form 0 cleaned_data: {'title': 'Test Track', 'duration': '00:61:00'}", log_output)
