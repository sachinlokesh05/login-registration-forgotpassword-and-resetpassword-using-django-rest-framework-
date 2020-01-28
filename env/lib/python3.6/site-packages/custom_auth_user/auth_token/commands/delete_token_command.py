# -*- coding: utf-8
# Models
from custom_auth_user.models import AuthToken


def delete_token(auth_token_store, token):
    try:
        token = auth_token_store.query_set.select_related(
            'user').filter_by_active().find_by_token(token)

        auth_token_store.delete(token)
    except AuthToken.DoesNotExist:
        return False

    return True
