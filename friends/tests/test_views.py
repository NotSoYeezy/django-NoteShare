from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class TestAddFriendView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        self.client.force_login(self.user)

        self.friend = get_user_model().objects.create(username='TestFriend', email='test2@test.pl')
        self.url = reverse('friends:add_friend', args=[self.friend.pk])

    def test_redirect_works(self):
        """Testing if user is redirected after adding friend"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_adding_friend_successful(self):
        """Testing if user can add friend"""
        response = self.client.get(self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.friends, [self.friend.username])


class TestRemoveFriendView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        self.client.force_login(self.user)

        self.friend = get_user_model().objects.create(username='TestFriend', email='test2@test.pl')
        self.user.friends = [self.friend]
        self.user.save()
        self.url = reverse('friends:remove_friend', args=[self.friend.pk])

    def test_redirect_works(self):
        """Testing if user is redirected after removing friend"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_removing_friend_successful(self):
        """Testing if user can remove friend"""
        response = self.client.get(self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.friends, [])
