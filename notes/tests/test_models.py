from django.test import TestCase
from django.contrib.auth import get_user_model
from notes.models import Note, Category, Rate
import datetime
from django.template.defaultfilters import slugify


class NoteModelTest(TestCase):

    def test_creating_category(self):
        """Testing if you can create category"""
        category_name = 'Test Category'
        category = Category.objects.create(name=category_name)
        self.assertEqual(category.name, category_name)

    def test_creating_note(self):
        """Testing if user can create note"""
        user = get_user_model().objects.create(username='User', email='test@test.pl')
        user.set_password('test123')
        category = Category.objects.create(name='test_category')

        note = Note.objects.create(author=user,
                                   category=category,
                                   title='Test title',
                                   thumbnail='thumbnails/kaktus.jpg',
                                   content_file='notes/Niemiecki.pdf'
                                   )

        self.assertEqual(note.author, user)
        self.assertEqual(note.category, category)
        self.assertEqual(note.title, 'Test title')
        self.assertEqual(note.thumbnail, 'thumbnails/kaktus.jpg')
        self.assertEqual(note.content_file, 'notes/Niemiecki.pdf')
        self.assertEqual(note.created_date.strftime('%Y-%m-%d'),
                         datetime.datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(note.slug, slugify(note.title))

    def test_creating_rate(self):
        """Testing if you can create rate for a note"""
        user = get_user_model().objects.create(username='User', email='test@test.pl')
        user.set_password('test123')
        category = Category.objects.create(name='test_category')
        note = Note.objects.create(author=user,
                                   category=category,
                                   title='Test title',
                                   thumbnail='thumbnails/kaktus.jpg',
                                   content_file='notes/Niemiecki.pdf'
                                   )

        rating = 4
        rate = Rate.objects.create(note=note, author=user, rate=rating)

        self.assertEqual(rate.note, note)
        self.assertEqual(rate.author, user)
        self.assertEqual(rate.rate, rating)

    def test_rating_change_successful(self):
        """Testing if note rating is updated after creating rate"""
        user = get_user_model().objects.create(username='User', email='test@test.pl')
        user.set_password('test123')
        rating_1 = 4
        rating_2 = 2
        category = Category.objects.create(name='test_category')
        note = Note.objects.create(author=user,
                                   category=category,
                                   title='Test title',
                                   thumbnail='thumbnails/kaktus.jpg',
                                   content_file='notes/Niemiecki.pdf'
                                   )
        rate_one = Rate.objects.create(note=note, author=user, rate=rating_1)
        note = Note.objects.get(author=user)
        self.assertEqual(note.rating, rate_one.rate)
        rate_two = Rate.objects.create(note=note, author=user, rate=rating_2)
        note = Note.objects.get(author=user)
        self.assertEqual(note.rating, (rating_1+rating_2)/2)  # Checking if rating is averaged
