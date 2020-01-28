# -*- coding: utf-8
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from custom_auth_user.user.manager import UserManager


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    Abstract user model
    """

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # User manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class User(AbstractUser):
    """
    User model extends AbstractUser
    """

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
