# -*- coding: utf-8
# Core
from django.utils.crypto import get_random_string

# Models
from custom_auth_user.models import AuthToken


class AuthTokenStore():
    """
    Auth token store
    """

    model = AuthToken
    query_set = AuthToken.objects

    def save(self, auth_token):
        auth_token.save()
        return auth_token

    def create(self, user):
        auth_token = self.model(
            token=self.generate_token(),
            user=user)
        auth_token.save()

        return auth_token

    def generate_token(self, token=None):
        if token is None:
            token = get_random_string(32)

        try:
            self.query_set.select_related('user').find_by_token(token)

            return self.generate_token()
        except AuthToken.DoesNotExist:
            return token

    def delete(self, token):
        token.delete()
