import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Series, Track


class SeriesUpdateViewTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@test.com', password='password')

        # Create test series
        self.series = Series.objects.create(title_en='Test Series', title_ru='Тестовая серия')

        # Create test tracks
        self.track1 = Track.objects.create(title_en='Track 1', title_ru='Трек 1', series=self.series, series_order=1)
        self.track2 = Track.objects.create(title_en='Track 2', title_ru='Трек 2', series=self.series, series_order=2)
        self.track3 = Track.objects.create(
            title_en='Track 3', title_ru='Трек 3', series=None  # Not in series initially
        )

    def test_update_tracks_success(self):
        """Test successful update of tracks in series."""
        self.client.login(username='admin', password='password')

        data = {
            'tracks': [
                {'id': self.track1.id, 'series_order': 2, 'delete': False},
                {'id': self.track2.id, 'series_order': 1, 'delete': False},
                {'id': self.track3.id, 'series_order': 3, 'delete': False},
            ]
        }

        url = reverse('admin:update_series_tracks', args=[self.series.id])
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(len(response_data['updated_tracks']), 3)

        # Refresh tracks from database
        self.track1.refresh_from_db()
        self.track2.refresh_from_db()
        self.track3.refresh_from_db()

        # Check series_order updates
        self.assertEqual(self.track1.series_order, 2)
        self.assertEqual(self.track2.series_order, 1)
        self.assertEqual(self.track3.series_order, 3)

        # Check series assignments
        self.assertEqual(self.track1.series, self.series)
        self.assertEqual(self.track2.series, self.series)
        self.assertEqual(self.track3.series, self.series)

    def test_delete_tracks(self):
        """Test deletion of tracks from series."""
        self.client.login(username='admin', password='password')

        data = {
            'tracks': [
                {'id': self.track1.id, 'series_order': 1, 'delete': False},
                {'id': self.track2.id, 'series_order': None, 'delete': True},
            ]
        }

        url = reverse('admin:update_series_tracks', args=[self.series.id])
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(len(response_data['deleted_tracks']), 1)
        self.assertEqual(response_data['deleted_tracks'][0], self.track2.id)

        # Refresh tracks from database
        self.track1.refresh_from_db()
        self.track2.refresh_from_db()

        # Check track1 is still in series
        self.assertEqual(self.track1.series, self.series)
        self.assertEqual(self.track1.series_order, 1)

        # Check track2 is removed from series
        self.assertIsNone(self.track2.series)
        self.assertIsNone(self.track2.series_order)

    def test_invalid_series(self):
        """Test request with invalid series ID."""
        self.client.login(username='admin', password='password')

        data = {'tracks': []}
        url = reverse('admin:update_series_tracks', args=[9999])  # Non-existent series
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Series not found')

    def test_invalid_json(self):
        """Test request with invalid JSON."""
        self.client.login(username='admin', password='password')

        url = reverse('admin:update_series_tracks', args=[self.series.id])
        response = self.client.post(url, data='invalid json', content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Invalid JSON data')

    def test_non_staff_user(self):
        """Test that non-staff users cannot access the endpoint."""
        # Create non-staff user
        regular_user = User.objects.create_user(username='user', email='user@test.com', password='password')
        self.client.login(username='user', password='password')

        data = {'tracks': []}
        url = reverse('admin:update_series_tracks', args=[self.series.id])
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403])

    def test_invalid_track_id(self):
        """Test handling of invalid track IDs."""
        self.client.login(username='admin', password='password')

        data = {
            'tracks': [
                {'id': 9999, 'series_order': 1, 'delete': False},  # Non-existent track
                {'id': self.track1.id, 'series_order': 2, 'delete': False},
            ]
        }

        url = reverse('admin:update_series_tracks', args=[self.series.id])
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        # Should only update the valid track
        self.assertEqual(len(response_data['updated_tracks']), 1)
        self.assertEqual(response_data['updated_tracks'][0]['id'], self.track1.id)

    def test_mixed_update_and_delete(self):
        """Test mixing updates and deletions in the same request."""
        self.client.login(username='admin', password='password')

        data = {
            'tracks': [
                {'id': self.track1.id, 'series_order': 3, 'delete': False},
                {'id': self.track2.id, 'series_order': None, 'delete': True},
                {'id': self.track3.id, 'series_order': 1, 'delete': False},
            ]
        }

        url = reverse('admin:update_series_tracks', args=[self.series.id])
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(len(response_data['updated_tracks']), 2)
        self.assertEqual(len(response_data['deleted_tracks']), 1)

        # Refresh tracks from database
        self.track1.refresh_from_db()
        self.track2.refresh_from_db()
        self.track3.refresh_from_db()

        # Check results
        self.assertEqual(self.track1.series_order, 3)
        self.assertEqual(self.track1.series, self.series)

        self.assertIsNone(self.track2.series)
        self.assertIsNone(self.track2.series_order)

        self.assertEqual(self.track3.series_order, 1)
        self.assertEqual(self.track3.series, self.series)
