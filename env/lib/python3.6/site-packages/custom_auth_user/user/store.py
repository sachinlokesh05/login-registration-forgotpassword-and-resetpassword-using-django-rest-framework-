# -*- coding: utf-8
# Models
from django.contrib.auth import get_user_model


class UserStore():
    """
    User store
    """

    model = get_user_model()
    query_set = get_user_model().objects

    def save(self, user):
        user.save()
        return user

    def create(self, email, username, first_name,
               last_name, password, defer=False):
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_disabled=False)

        user.set_password(password)

        if not defer:
            user.save()

        return user
