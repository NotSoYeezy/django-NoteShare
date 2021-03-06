from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.contrib.postgres.fields import ArrayField


# TODO: Dodaj usuwanie profilowego z dysku
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100, primary_key=True)
    display_name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=100)
    bio = models.TextField(blank=True, max_length=600, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    friends = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if self.display_name is None:
            self.display_name = self.username

        super(User, self).save(*args, **kwargs)
