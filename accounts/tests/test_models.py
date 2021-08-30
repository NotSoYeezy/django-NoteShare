from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class ModelTest(TestCase):

    def test_creating_user_successful(self):
        """Checking if user is creates"""
        username = 'marcin'
        email = 'test@test.pl'
        password = 'test123'

        user = get_user_model().objects.create(username=username, email=email)
        user.set_password(password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
