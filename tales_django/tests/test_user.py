from typing import Optional

from django.test import TestCase
from django.contrib.auth.models import User

# from myapp.models import Animal

# @see https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing


class Test_user(TestCase):
    # @classmethod
    # def setUpTestData(cls):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dummy_false_is_false(self):
        print('Method: test_false_is_false.')
        self.assertFalse(False)

    def test_user_create_and_remove(self):
        user: Optional[User]
        try:
            """
            Sample test
            """
            # lion = Animal.objects.get(name="lion")
            # cat = Animal.objects.get(name="cat")
            # self.assertEqual(lion.speak(), 'The lion says "roar"')
            # self.assertEqual(cat.speak(), 'The cat says "meow"')

            user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            user.last_name = 'Lennon'
            user.save()

            # Should have integer id
            self.assertIsInstance(user.id, int)
        finally:
            if user:
                user.delete()
