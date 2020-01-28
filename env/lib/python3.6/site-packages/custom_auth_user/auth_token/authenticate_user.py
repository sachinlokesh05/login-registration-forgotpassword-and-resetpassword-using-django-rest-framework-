# -*- coding: utf-8
# Exception
from custom_auth_user.auth_token.exceptions import AuthenticationFailed

# Stores
from custom_auth_user.auth_token.store import AuthTokenStore
from custom_auth_user.user.store import UserStore

# Commands
from custom_auth_user.auth_token.commands.authenticate_user_command \
    import authenticate_user
from custom_auth_user.auth_token.commands.create_auth_token_command \
    import create_auth_token


class AuthenticateUserService():
    """
    Authenticate user service
    """

    auth_token_store = AuthTokenStore()
    user_store = UserStore()

    def __init__(self, email_or_username, password):
        self.email_or_username = email_or_username
        self.password = password

    def run(self):
        user = authenticate_user(
            user_store=self.user_store,
            email_or_username=self.email_or_username,
            password=self.password)

        if not user:
            raise AuthenticationFailed

        auth_token = create_auth_token(self.auth_token_store, user)

        return auth_token
