from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class TestAdminPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create(username='AdminUser', email='test@test.pl')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)

    def test_added_fieldsets(self):
        """Testing if added fieldsets work"""
        user = get_user_model().objects.create(username='TestUser', email='user@user.pl')
        user.bio = 'Test BIO'
        user.friends = ['Test Friend',]
        user.save()
        url = reverse('admin:accounts_user_change', args=[user.pk])
        response = self.client.get(url)

        self.assertContains(response, 'Test BIO')
        self.assertContains(response, 'Test Friend')
        self.assertContains(response, 'profile_pic')



