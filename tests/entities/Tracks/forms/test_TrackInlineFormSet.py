from unittest.mock import Mock, patch

import pytest
from django.forms import BaseInlineFormSet

from tales_django.entities.Tracks.forms.TrackInlineFormSet import TrackInlineFormSet


@pytest.fixture
def mock_formset():
    """Fixture to create a TrackInlineFormSet instance with mocked dependencies."""
    formset = TrackInlineFormSet(data={}, files={}, prefix='test_prefix')
    # Mock formset forms for consistent testing
    formset.forms = [
        Mock(is_bound=True, is_valid=lambda: True, errors={}, cleaned_data={'name': 'Test Track'}),
        Mock(is_bound=False, is_valid=lambda: False, errors={'field': ['error']}),
    ]
    return formset


def test_is_valid_returns_true(mock_formset, caplog):
    """Test is_valid returns True and logs correct information."""
    with patch.object(BaseInlineFormSet, 'is_valid', return_value=True):
        result = mock_formset.is_valid()

        # Assert result
        assert result is True

        # Assert logs
        assert 'TrackInlineFormSet.is_valid() called' in caplog.text
        assert 'Formset management data: TOTAL=N/A, INITIAL=N/A' in caplog.text
        assert 'Forms bound status: [True, False]' in caplog.text
        assert 'TrackInlineFormSet.is_valid() returned: True' in caplog.text


def test_is_valid_returns_false(mock_formset, caplog):
    """Test is_valid returns False and logs error information."""
    with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
        result = mock_formset.is_valid()

        # Assert result
        assert result is False

        # Assert error logs
        assert 'Formset errors:' in caplog.text
        assert 'Formset non-field errors:' in caplog.text
        assert 'Form 0 is valid: True, bound: True' in caplog.text
        assert "Form 1 errors: {'field': ['error']}" in caplog.text


def test_is_valid_with_bound_forms(mock_formset, caplog):
    """Test is_valid correctly logs form bound status."""
    # Update form bound status
    mock_formset.forms = [
        Mock(is_bound=True, is_valid=lambda: True, errors={}),
        Mock(is_bound=True, is_valid=lambda: False, errors={'name': ['required']}),
    ]

    with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
        mock_formset.is_valid()

        # Assert bound status logs
        assert 'Forms bound status: [True, True]' in caplog.text
        assert 'Form 1 non-field errors:' in caplog.text
        assert 'Form 1 cleaned_data: No cleaned_data' not in caplog.text  # Should not appear if form has errors


def test_is_valid_with_unbound_forms(mock_formset, caplog):
    """Test is_valid handles unbound forms correctly."""
    # Update form bound status
    mock_formset.forms = [
        Mock(is_bound=False, is_valid=lambda: False, errors={}),
        Mock(is_bound=False, is_valid=lambda: False, errors={}),
    ]

    with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
        mock_formset.is_valid()

        # Assert logs for unbound forms
        assert 'Forms bound status: [False, False]' in caplog.text
        assert 'Form 0 is valid: False, bound: False' in caplog.text
        assert 'Form 1 is valid: False, bound: False' in caplog.text


def test_is_valid_with_management_data(caplog):
    """Test is_valid correctly logs management data (TOTAL_FORMS/INITIAL_FORMS)."""
    # Create formset with management data in input
    data = {'test_prefix-TOTAL_FORMS': '5', 'test_prefix-INITIAL_FORMS': '2'}
    formset = TrackInlineFormSet(data=data, files={}, prefix='test_prefix')
    formset.forms = [
        Mock(is_bound=True, is_valid=lambda: True, errors={}),
        Mock(is_bound=True, is_valid=lambda: True, errors={}),
        Mock(is_bound=False, is_valid=lambda: False, errors={}),
        Mock(is_bound=False, is_valid=lambda: False, errors={}),
        Mock(is_bound=False, is_valid=lambda: False, errors={}),
    ]

    with patch.object(BaseInlineFormSet, 'is_valid', return_value=True):
        formset.is_valid()

    # Verify management data logs
    assert 'Formset management data: TOTAL=5, INITIAL=2' in caplog.text


def test_is_valid_with_formset_non_field_errors(mock_formset, caplog):
    """Test is_valid logs formset-level non-field errors."""
    # Mock formset non-field errors
    mock_formset.non_form_errors = Mock(return_value=['Global validation error'])

    with patch.object(BaseInlineFormSet, 'is_valid', return_value=False):
        mock_formset.is_valid()

    # Verify non-field errors logs
    assert "Formset non-field errors: ['Global validation error']" in caplog.text


def test_is_valid_with_bound_invalid_form_cleaned_data(caplog):
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
        formset.is_valid()

    # Verify cleaned_data logs
    assert "Form 0 non-field errors: ['Form-level validation error']" in caplog.text
    assert "Form 0 cleaned_data: {'title': 'Test Track', 'duration': '00:61:00'}" in caplog.text
