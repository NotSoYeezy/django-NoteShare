from django.test import TestCase
from accounts.forms import UserSignupForm, UserPasswordResetForm, UserSetPasswordForm, UserChangePassword
from django.contrib.auth import get_user_model


class FormTest(TestCase):
    """Testing only signup form, others are taken from django user management system"""
    def test_signup_form_valid(self):
        """Testing if UserSignupForm is valid"""
        form_data = {'username': 'Test user',
                     'display_name': 'Test display',
                     'email': 'test@test.pl',
                     'password': 'TestPassword123',
                     'confirm_password': 'TestPassword123',
                     }
        form = UserSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'Test user')
        self.assertEqual(form.cleaned_data['display_name'], 'Test display')
        self.assertEqual(form.cleaned_data['email'], 'test@test.pl')
        self.assertEqual(form.cleaned_data['password'], 'TestPassword123')
        self.assertEqual(form.cleaned_data['confirm_password'], 'TestPassword123')

    def test_signup_form_save(self):
        """Testing if you can save UserSignupForm and create user with that"""
        form_data = {'username': 'Test user',
                     'display_name': 'Test display',
                     'email': 'test@test.pl',
                     'password': 'TestPassword123',
                     'confirm_password': 'TestPassword123',
                     }
        form = UserSignupForm(data=form_data)
        form.save()
        user = get_user_model().objects.get(username='Test user')
        user.set_password(form.cleaned_data['password'])

        self.assertEqual(user.username, 'Test user')
        self.assertEqual(user.display_name, 'Test display'),
        self.assertEqual(user.email, 'test@test.pl'),
        self.assertEqual(user.profile_pic, 'profile_pics/default.png')  # Checking if user saves with default pfp
        self.assertTrue(user.check_password(form.cleaned_data['password']))