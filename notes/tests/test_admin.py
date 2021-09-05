from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='Test user', email='test@test.pl')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        self.url = reverse('admin:index')

    def test_category_model_registered(self):
        """Testing if category model is registered on admin site"""
        response = self.client.get(self.url)

        self.assertContains(response, 'Category')

    def test_note_model_registered(self):
        """Testing if note model is registered on admin site"""
        response = self.client.get(self.url)

        self.assertContains(response, 'Note')

    def test_rate_model_registered(self):
        """Testing if rate model is registered on admin site"""
        response = self.client.get(self.url)

        self.assertContains(response, 'Note')