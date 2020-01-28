# -*- coding: utf-8
# pylint: disable=W0622

from django.utils import timezone
from django.db import models


class AuthTokenQueryset(models.query.QuerySet):
    """
    Auth token query set
    """

    def get_all(self):
        return self.all()

    def find_by_id(self, id):
        return self.get(id=id)

    def find_by_token(self, token):
        return self.get(token=token)

    def filter_by_active(self):
        return self.filter(expiration_date__gte=timezone.now())

    def filter_by_expired(self):
        return self.filter(expiration_date__lt=timezone.now())


class AuthTokenManager(models.Manager):
    """
    Auth token manager
    """

    def get_queryset(self):
        return AuthTokenQueryset(self.model, using=self._db)

    def get_all(self):
        return self.get_queryset().get_all()

    def find_by_id(self, id):
        return self.get_queryset().find_by_id(id)

    def find_by_token(self, token):
        return self.get_queryset().find_by_token(token)

    def filter_by_active(self):
        return self.get_queryset().filter_by_active()

    def filter_by_expired(self):
        return self.get_queryset().filter_by_expired()
