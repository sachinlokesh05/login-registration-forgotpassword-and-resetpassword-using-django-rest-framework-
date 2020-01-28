# -*- coding: utf-8
# pylint: disable=W0622

# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class UserQueryset(models.query.QuerySet):
    """
    User query set
    """

    def get_all(self):
        return self.all()

    def find_by_id(self, id):
        return self.get(id=id)

    def find_by_username(self, username):
        return self.get(username=username)

    def find_by_email(self, email):
        return self.get(email=email)

    # Filter by active
    def filter_by_active(self):
        return self.filter(is_active=True)

    def filter_by_inactive(self):
        return self.filter(is_active=False)

    # Filter by enable
    def filter_by_enabled(self):
        return self.filter(is_disabled=False)

    def filter_by_disabled(self):
        return self.filter(is_disabled=True)


class UserManager(BaseUserManager):
    """
    User manager
    """

    def _create_user(self, email, password, is_staff,
                     is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def get_all(self):
        return self.get_queryset().get_all()

    def find_by_id(self, id):
        return self.get_queryset().find_by_id(id)

    def find_by_username(self, username):
        return self.get_queryset().find_by_username(username)

    def find_by_email(self, email):
        return self.get_queryset().find_by_email(email)

    # Filter by active
    def filter_by_active(self):
        return self.get_queryset().filter_by_active()

    def filter_by_inactive(self):
        return self.get_queryset().filter_by_inactive()

    # Filter by enable
    def filter_by_enabled(self):
        return self.get_queryset().filter_by_enabled()

    def filter_by_disabled(self):
        return self.get_queryset().filter_by_disabled()
