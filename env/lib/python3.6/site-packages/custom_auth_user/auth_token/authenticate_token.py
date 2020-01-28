# -*- coding: utf-8
# Exception
from custom_auth_user.auth_token.exceptions import AuthenticationFailed

# Stores
from custom_auth_user.auth_token.store import AuthTokenStore

# Commands
from custom_auth_user.auth_token.commands.authenticate_token_command \
    import authenticate_token


class AuthenticateTokenService():
    """
    Authenticate token service
    """

    auth_token_store = AuthTokenStore()

    def __init__(self, auth_token):
        self.auth_token = auth_token

    def run(self):
        user = authenticate_token(
            auth_token_store=self.auth_token_store,
            auth_token=self.auth_token)

        if not user:
            raise AuthenticationFailed

        return user
