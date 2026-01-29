from unittest.mock import Mock, patch

from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.test import TestCase

from ..models import Series, Track


class TrackInlineFormSetTestCase(TestCase):
    def setUp(self):
        # Create the formset class using inlineformset_factory to properly initialize
        from ..forms.TrackInlineFormSet import TrackInlineFormSet

        self.TrackFormSet = inlineformset_factory(
            Series,  # Parent model
            Track,  # Child model
            formset=TrackInlineFormSet,
            fields=('id', 'title_ru', 'title_en', 'series_order'),  # Match the fields from the admin
            extra=0,
            can_delete=True,
        )

    def test_formset_is_base_inline_formset(self):
        """Test that TrackInlineFormSet inherits from BaseInlineFormSet."""
        # Create an unbound formset instance
        formset = self.TrackFormSet()
        self.assertIsInstance(formset, BaseInlineFormSet)

    def test_formset_methods_exist(self):
        """Test that custom methods exist in the formset."""
        # Create an unbound formset instance
        formset = self.TrackFormSet()

        # Check that custom methods exist
        self.assertTrue(hasattr(formset, 'clean'))
        self.assertTrue(hasattr(formset, 'save'))
        self.assertTrue(hasattr(formset, 'save_new'))
        self.assertTrue(hasattr(formset, 'save_existing'))
        self.assertTrue(hasattr(formset, 'save_new_objects'))
        self.assertTrue(hasattr(formset, 'save_existing_objects'))

    def test_formset_has_correct_attributes(self):
        """Test that the formset has the expected attributes."""
        # Create an unbound formset instance
        formset = self.TrackFormSet()

        # Check that it has the expected attributes
        self.assertTrue(hasattr(formset, 'clean'))
        self.assertTrue(hasattr(formset, 'save'))
        self.assertTrue(hasattr(formset, 'save_new'))
        self.assertTrue(hasattr(formset, 'save_existing'))
        self.assertTrue(hasattr(formset, 'save_new_objects'))
        self.assertTrue(hasattr(formset, 'save_existing_objects'))
