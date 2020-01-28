# -*- coding: utf-8
# Exception
from custom_auth_user.auth_token.exceptions \
    import TokenNotFound

# Stores
from custom_auth_user.auth_token.store import AuthTokenStore

# Commands
from custom_auth_user.auth_token.commands.delete_token_command \
    import delete_token


class DeleteTokenService():
    """
    Delete token service
    """

    auth_token_store = AuthTokenStore()

    def __init__(self, token):
        self.token = token

    def run(self):
        is_token_deleted = delete_token(
            auth_token_store=self.auth_token_store, token=self.token)

        if is_token_deleted is False:
            raise TokenNotFound

        return
