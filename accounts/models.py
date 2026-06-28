from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
        ROLE_CHOICES=(
                ('doctor','Doctor'),
                ('patient','Patient'),
                    )
        role=models.CharField(
            max_length=10,
            choices=ROLE_CHOICES
        )
        google_token = models.TextField(blank=True, null=True)
        google_refresh_token = models.TextField(blank=True, null=True)
        google_token_uri = models.CharField(max_length=255, blank=True, null=True)
        google_credentials = models.TextField(blank=True, null=True)