from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.
class User(AbstractUser):
    username = models.CharField(unique=True, primary_key=True, max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    bio = models.TextField(blank=True, max_length=600, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pics')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk':self.pk})
