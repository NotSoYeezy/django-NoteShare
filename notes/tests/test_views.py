from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from notes.models import Note, Category, Rate
from django.shortcuts import reverse
from notes.forms import RateForm
from notes.views import NoteCreateView


class TestNoteDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
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
        self.url = reverse('notes:detail_note', args=[self.note.slug])

    def test_context_data(self):
        """Testing if context data is passed correctly"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['note'], self.note)
        self.assertEqual(response.context['form'], RateForm)
        self.assertEqual(response.context['user_rate'], 0)

    def test_note_render_successfully(self):
        """Test if note renders successfully"""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.category)

    def test_note_rate_form_works(self):
        """Test if user can submit rate form"""

        self.client.force_login(self.user)
        post_data = {'rate': 3}
        self.client.post(self.url, post_data)
        updated_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(updated_note.rating, 3)

    def test_note_rate_update_works(self):
        """Test if user can update rating that was made before"""

        self.client.force_login(self.user)
        post_data = {'rate': 4}
        rating = Rate.objects.create(note=self.note, author=self.user, rate='2')
        self.client.post(self.url, post_data)
        note_updated = Note.objects.get(slug=self.note.slug)
        self.assertEqual(note_updated.rating, 4)


class TestNoteDeleteView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='TestUser', email='test@test.pl')
        self.user.set_password('TestPassword123')
        self.user.save()
        self.client.force_login(self.user)
        self.category = Category.objects.create(name='TestCategory')
        self.note = Note.objects.create(
            author=self.user,
            category=self.category,
            title='TestTitle',
            thumbnail='thumbnails/test.jpg',
            content_file='notes/test.pdf',
        )
        self.url = reverse('notes:delete_note', args=[self.note.slug])

    def test_context_data(self):
        """Testing if context data is passed correctly"""
        response = self.client.get(self.url)

        self.assertEqual(response.context['note'], self.note)
        self.assertEqual(response.context['error'], '')

    def test_note_delete_successful(self):
        """Testing if note can be deleted"""
        post_data = {'rdo': 'Yes'}
        self.client.post(self.url, post_data)

        with self.assertRaises(Note.DoesNotExist):
            note = Note.objects.get(slug=self.note.slug)

    def test_redirect_after_no_choice_successful(self):
        """Testing if user is redirected after selecting 'No' option"""
        post_data = {'rdo': 'No'}
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)

    def test_error_returns_successful(self):
        """Testing if after passing other post data view returns error"""
        post_data = {'rdo': 'wrong_data'}
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.context['error'], 'There was an error, please try again')

