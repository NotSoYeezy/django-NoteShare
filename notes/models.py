from django.db import models
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django_unique_slugify import unique_slugify

# Własne importy
from .validators import check_file_extension
from docx2pdf import convert


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Category list'


class Note(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnails')
    content_file = models.FileField(upload_to='notes', blank=True, null=True, validators=[check_file_extension])
    content_text = models.TextField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
