from django.test import TestCase
from profiles.forms import UserUpdateForm
from django.contrib.auth import get_user_model


class TestUserUpdateForm(TestCase):

    def setUp(self):
        self.form_data = {
            'display_name': 'TestDisplay',
            'bio': 'TestBio',
            'profile_pic': 'profile_pictures/test.jpg',
        }

    def test_form_is_valid(self):
        """Testing if form is valid"""
        form = UserUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_when_bad_data(self):
        """Testing if form is not valid when passing wrong data"""
        wrong_form_data = {
            'display_name': '',
            'bio': '',
            'profile_pic': ''
        }
        form = UserUpdateForm(data=wrong_form_data)
        self.assertFalse(form.is_valid())
