from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username