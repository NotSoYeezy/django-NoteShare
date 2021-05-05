from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pics')

    def __str__(self):
        return self.username
