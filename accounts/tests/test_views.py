from django.test import TestCase, Client
from accounts.models import User
from django.shortcuts import reverse
from django.contrib.auth import get_user_model, get_user
from accounts.forms import UserSignupForm, UserChangePassword


class TestLogoutView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')

        self.client.force_login(self.user)

    def test_logout_successful(self):
        """Test that logout view works"""
        url = reverse('accounts:logout')
        self.client.get(url)

        self.assertNotIn('_auth_user_id', self.client.session)


class TestUserRegisterView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_context(self):
        """Testing if context data is right"""
        url = reverse('accounts:register')
        user_form = UserSignupForm
        response = self.client.get(url)

        self.assertEqual(response.context['user_form'], user_form)
        self.assertFalse(response.context['registered'])

    def test_registration_successful(self):
        """Test if user can register using register view"""
        url = reverse('accounts:register')
        post_data = {'username': 'Test user',
                     'display_name': 'Test display',
                     'email': 'test@test.pl',
                     'password': 'TestPassword123',
                     'confirm_password': 'TestPassword123'}

        response = self.client.post(url, post_data)

        user = get_user_model().objects.get(username='Test user')
        self.assertTrue(user)
        self.assertEqual(user.username, 'Test user')
        self.assertEqual(user.display_name, 'Test display')
        self.assertEqual(user.email, 'test@test.pl')
        self.assertTrue(user.check_password('TestPassword123'))
        self.assertTrue(response.context['registered'])


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_successful(self):
        """Test if user can login"""
        url = reverse('accounts:login')
        user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        user.set_password('TestPassword123')
        user.save()

        post_data = {'username': 'TestUser',
                     'password': 'TestPassword123'}

        response = self.client.post(url, post_data)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(response.url, '/')

    def test_login_error_context_data(self):
        """Test if error_tag shows after wrong login"""
        url = reverse('accounts:login')
        user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        user.set_password('TestPassword123')
        user.save()

        post_data = {'username': 'TestUser',
                     'password': 'WrongPassword'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.context['error_tag'], 'Wrong credentials, try again')


class TestChangePasswordView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        self.user.set_password('TestPassword123')
        self.user.save()

        self.client.force_login(self.user)

    def test_change_password_successful(self):
        """Testing if user can change password"""
        url = reverse('accounts:change_password')
        post_data = {'old_password': 'TestPassword123',
                     'new_password1': 'NewPassword123',
                     'new_password2': 'NewPassword123'}
        response = self.client.post(url, post_data)
        user = get_user_model().objects.get(username='TestUser')
        self.assertTrue(user.check_password('NewPassword123'))


class TestDeleteAccountView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        self.user.set_password('TestPassword123')
        self.user.save()
        self.client.force_login(self.user)
        self.url = reverse('accounts:delete_account')

    def test_delete_account_successful(self):
        """Test if user can delete account successfully"""
        post_data = {'rdo': 'Yes'}
        response = self.client.post(self.url, post_data)

        with self.assertRaises(User.DoesNotExist):
            user = get_user_model().objects.get(username='TestUser')

    def test_delete_account_deny(self):
        """Test if user can deny account deletion"""
        url = reverse('accounts:delete_account')
        post_data = {'rdo': 'No'}
        response = self.client.post(self.url, post_data)

        self.assertTrue(get_user_model().objects.get(username='TestUser'))

    def test_error_returns_successful(self):
        """Testing if after passing wrong post data view returns correct error"""
        post_data = {'rdo': 'wrong_data'}
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.context['error'], 'There was an error, please try again')
