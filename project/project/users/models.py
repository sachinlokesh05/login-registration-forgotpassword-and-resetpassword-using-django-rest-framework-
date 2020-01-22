from django.db import models
from django.contrib.auth import get_user_model


class Registration(models.Model):
    username = models.CharField(blank=False, max_length=100)
    email = models.EmailField(blank=True)
    password1 = models.CharField(max_length=60)
    password2 = models.CharField(max_length=50)

    def __str__(self):
        return self.username
