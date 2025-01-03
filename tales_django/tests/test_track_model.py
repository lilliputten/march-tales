from typing import Optional

from django.test import TestCase

from tales_django.models import Track

# from django.contrib.models import Track

# from myapp.models import Animal

# @see https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing


class Test_Track(TestCase):
    # @classmethod
    # def setUpTestData(cls):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_track_dummy_false_is_false(self):
        # print('Method: Test_Track_dummy_false_is_false.')
        self.assertFalse(False)

    def test_track_create_and_remove(self):
        track: Optional[Track] = None
        try:
            """
            Sample test
            """
            track = Track.objects.create(
                title='Test title',
                created_by_id=1,
                updated_by_id=1,
            )
            # track.last_name = 'Lennon'
            track.save()

            # Should have integer id
            self.assertIsInstance(track.id, int)
        finally:
            if track:
                track.delete()
