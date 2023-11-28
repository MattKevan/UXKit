from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='user_profiles/', null=True, blank=True)

    def __str__(self):
        return self.email