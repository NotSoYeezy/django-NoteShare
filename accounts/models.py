from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    bio = models.TextField(blank=True, max_length=600)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pics')

    def __str__(self):
        return self.username
