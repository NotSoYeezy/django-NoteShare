from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class TestUrls(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='Test user', email="test@test.pl")
        self.client = Client()

    def test_login_url_render_successfully(self):
        """Testing if login url renders successfully"""
        url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_logout_url_works_successfully(self):
        """Testing if logout url redirects to index successfully"""
        url = reverse('accounts:logout')
        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_signup_url_render_successfully(self):
        """Testing if signup url renders successfully"""
        url = reverse('accounts:register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_change_password_url_render_successfully(self):
        """Testing if change password url renders successfully"""
        self.client.force_login(self.user)
        url = reverse('accounts:change_password')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_delete_account_url_render_successfully(self):
        """Testing if delete account url renders successfully"""
        self.client.force_login(self.user)
        url = reverse('accounts:delete_account')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)