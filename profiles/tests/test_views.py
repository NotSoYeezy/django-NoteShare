from django.test import TestCase, Client
from notes.models import Category, Note
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.core.paginator import Paginator

# Not testing update user view because it's Django Generic View without any changes


class TestUserProfileView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl', bio='test Bio')
        self.user.set_password('TestPassword123')
        self.user.save()
        self.category = Category.objects.create(name='TestCategory')
        self.note = Note.objects.create(
            author=self.user,
            category=self.category,
            title='TestTitle',
            thumbnail='thumbnails/test.jpg',
            content_file='notes/test.pdf',
        )
        self.url = reverse('profile', args=[self.user.pk])

    def test_page_renders_successfully(self):
        """Testing if user profile page renders successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_data_passed(self):
        """Testing if context data is passed correctly"""
        response = self.client.get(self.url)
        paginator = Paginator(Note.objects.filter(author=self.user), 1)
        self.assertEqual(response.context['user_profile'], self.user)
        self.assertEqual(response.context['total_friends'], 0)
        self.assertEqual(response.context['total_followers'], 0)
        self.assertEqual(response.context['notes'].number, paginator.page(1).number)

    def test_note_renders_successfully(self):
        """Testing if note renders on user page"""
        response = self.client.get(self.url)
        self.assertContains(response, self.note)

    def test_user_data_renders_successfully(self):
        """Testing if user data renders correctly on user page"""
        response = self.client.get(self.url)
        self.assertContains(response, self.user.display_name)
        self.assertContains(response, self.user.bio)
        self.assertContains(response, self.user.profile_pic)


class TestUserFollowingList(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')

        self.category = Category.objects.create(name='TestCategory')
        self.note = Note.objects.create(
            author=self.user,
            category=self.category,
            title='TestTitle',
            thumbnail='thumbnails/test.jpg',
            content_file='notes/test.pdf',
        )

        self.following_user = get_user_model().objects.create(username='TestFollowing', email="test2@test.pl")
        self.user.friends = [self.following_user, ]
        self.user.save()

        self.url = reverse('following_list', args=[self.user.pk])

    def test_page_renders_successfully(self):
        """Testing if page renders successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_data_correct(self):
        """Testing if context data is correctly passed"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['users_following'], [self.user.friends[0]])

    def test_context_data_correct_when_no_one_is_following(self):
        """Testing if context data is correctly passed when user doesn't follow anyone"""
        self.user.friends = []
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.context['users_following'], [])

    def test_following_user_render_successfully(self):
        """Testing if following user is rendered successfully"""
        response = self.client.get(self.url)
        self.assertContains(response, self.user.friends[0])


class TestFollowersList(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')

        self.category = Category.objects.create(name='TestCategory')
        self.note = Note.objects.create(
            author=self.user,
            category=self.category,
            title='TestTitle',
            thumbnail='thumbnails/test.jpg',
            content_file='notes/test.pdf',
        )

        self.follower = get_user_model().objects.create(username='TestFollower', email="test2@test.pl")
        self.follower.friends = [self.user, ]
        self.follower.save()

        self.url = reverse('followers_list', args=[self.user.pk])

    def test_page_renders_successfully(self):
        """Testing if page renders successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_data_correct(self):
        """Testing if context data is passed correctly"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['followers'][0], self.follower)
        self.assertEqual(response.context['followed_user'], self.user)

    def test_context_data_correct_when_no_followers(self):
        """Testing if context data is passed correctly when user has no followers"""
        self.follower.friends = []
        self.follower.save()
        response = self.client.get(self.url)
        self.assertEqual(str(response.context['followers']), '<QuerySet []>')

    def test_followers_render_successfully(self):
        """Testing if followers are rendered successfully"""
        response = self.client.get(self.url)
        self.assertContains(response, self.follower.username)

